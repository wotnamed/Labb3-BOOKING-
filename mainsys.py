import json
import os

#  running parameters
clear_enabled = False  # Determines if the clear() function is ran upon each user input cycle. Can be changed by user.


def clear(status):  # Prompts the command line interface to clear the terminal. Does not work in an IDE.
    if status:
        os.system("cls||clear")  # 'cls' is used by Windows and 'clear' by Linux. (Linux hasn't been tested though.)


def get_data(file_name):
    """Loads the data from the file given in 'file_name'.

            Parameters
            ----------
            file_name : string, mandatory
                Name of the file to load data from.

            Returns
            ------
            data_list : list of dicts
                The JSON data loaded into a list.

            Raises
            ------
            FileNotFoundError
                If the JSON file was not found.
            ValueError
                If the file was not a valid JSON file.
            """
    try:
        with open(file_name, "r") as file:  # 'r' ensures we don't overwrite the file. 'r' for read, 'w' for write.
            data_list = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"{file_name} not found.")
    except json.JSONDecodeError:
        raise ValueError(f"{file_name} is not a valid JSON file.")

    return data_list

def is_invalid_data(dataset):  # Checks for incompatibility or corruption.
    if not isinstance(dataset, list) and not all(isinstance(i, dict) for i in dataset):
        return True  # The line above checks if the dataset isn't a list and if every item in the list isn't a dict.

    elif len(dataset) == 0:  # If the dataset has a length of zero, it doesn't contain any information.
        return True

    else: return False  # return False means that this function didn't flag the dataset as being "invalid".

def display_hotels(hotels_data):
    """ Prints every hotel and its data.

    The hotel name is printed in a rubric-like manner, as the data for each hotel is indented under the name.

    Parameters
    ----------
    hotels_data : list, mandatory
        The list of hotels, in which each hotel is a dictionary with key:value pairs.

    Raises
    ------
    ValueError
        Invalid hotels dataset was provided, ex. it is not a list of dictionaries.
    ValueError
        Any other unexpected errors that are raised during the printing process. Could be for example that the dictionaries includes only keys and no values.
    """

    if is_invalid_data(hotels_data):
        raise ValueError('An error occurred in the loading of hotels data. Invalid hotels data provided.')

    try:
        for h in hotels_data:  # For every hotel

            keys = list(h.keys())  # Find key
            hotel = list(h.values())  # Find value

            for p in range(len(hotel)):
                if p == 0:  # The first key:value pair in each hotel is the name. The key isn't printed here ('name').
                    print(f'{hotel[p]}')  # We don't indent the name to make it appear as a rubric.
                else:
                    print(f'    {keys[p]}: {hotel[p]}')  # All other key:value pairs are indented under the hotel name.
            print()  # New line to separate hotels from each other. Improves readability.
    except AttributeError:
        raise ValueError('An unexpected error occurred while printing the hotels data.')


def sort_hotels(hotels_data, k, reverse):
    """Sorts the 'hotels' dataset using the key and order inputted.

        Parameters
        ----------
        hotels_data : list of dicts, mandatory
            The hotels dataset to be used to sort
        k : string, mandatory
            Input for which key to sort with.
        reverse : boolean, mandatory
            Determines if the sorting order should be reversed, i.e. True if to be sorted in descending order.

        Returns
        ------
        hotels_data : list of dicts
            The sorted 'hotels' dataset.

        Raises
        ------
        ValueError
            Raised if the key for which the dataset should be sorted with could not be found.
        """

    def a(i):  # Extract key to be sorted
        try:
            return i[k]
        except KeyError:  # Catch error to prevent program crash.
            pass

    try:
        hotels_data.sort(reverse=reverse, key=a)  # Docs: https://docs.python.org/3.8/library/stdtypes.html#list.sort
        return hotels_data
    except TypeError:
        raise ValueError("List cannot be sorted by that property.")


def search_by_location(hotels_data, location):
    """Searches through the dataset and prints hotels that match the location inputted.

        Parameters
        ----------
        hotels_data : list of dicts, mandatory
            The hotels dataset to be used to search through.
        location : string
            The location to search for.

        Returns
        ------
        None

        Raises
        ------
        ValueError
            Is raised if no matching hotels were found in the given location.
    """
    hotels = [item for item in hotels_data if location.lower() in item['location'].lower()]  # Find hotels by location
    if not hotels:  # If no hotel were to be found (hotels list is empty or is False)
        raise ValueError('No hotels found in given location.')

    display_hotels(hotels)


def remove_booking(hotels_data, bookings_data):
    """Removes a booking specified by the user in bookings_data, by index of the booking in the list.

    Also corrects for the recovered rooms in the hotels_data database.

    Parameters
    ----------
    hotels_data : list of dicts, mandatory
        The hotels database
    bookings_data : list of dicts, mandatory
        The bookings database

    Raises
    ------
    ValueError
        The hotel found in the booking is not present in the hotel database.
    """
    print("Choose a booking to be removed.")
    display_bookings(bookings_data, True)
    index_of_booking = int(input("Please provide the index of the booking to be removed: "))
    hotel = bookings_data[index_of_booking]["hotel"]  # Find the hotel booked in the booking.
    rooms_of_booking = int(bookings_data[index_of_booking]["rooms booked"])  # Find the number of rooms booked.

    try:  # Find hotel by name using lambda. (Assure hotel exists)
        hotel = list(filter(lambda hotels_data : hotels_data['name'].lower() == hotel.lower(), hotels_data))[0]
    except IndexError:
        raise ValueError('Hotel does not exist.')

    hotels_data[hotels_data.index(hotel)]['rooms_available'] += rooms_of_booking  # Return unbooked rooms to hotel.
    bookings_data.pop(index_of_booking)  # Remove the booking from bookings_data.
    save(bookings_data, hotels_data)
    print("Booking successfully removed.")

def create_booking_dict(user, hotel, nights, rooms, total_cost):  # Used to be found within create_booking().
    new_booking = {
        "booking name": user,
        "hotel": hotel,
        "nights booked": nights,
        "rooms booked": rooms,
        "total cost": total_cost
    }

    return new_booking

def create_booking(hotels_data, bookings_data, f_save, user, hotel, nights, rooms, confirmation):
    """Creates a booking in the bookings_data database.

    Also adjusts the number of available rooms in the hotel_data database for the hotel booked by the user.

    The Legacy version of this function made the details of the booking be provided via the user in the terminal.
    This is no longer the case due to testing issues.

    Parameters
    ----------
    hotels_data : list of dicts, mandatory
        The hotel database
    bookings_data : list of dicts, mandatory
        The bookings database
    f_save : boolean, mandatory
        Specifies if the function calls the save() function or not. Set to False when testing, but True otherwise.
    user : str, mandatory
        "booking name" in the bookings file.
    hotel : str, mandatory
        The hotel to be booked. A basic search function has been implemented to account for search errors.
    nights : int, mandatory
        The number of nights desired to be booked
    rooms : int, mandatory
        The number of rooms desired to be booked.
    confirmation: str, mandatory
        User confirmation for the booking (Somewhat useless in the current implementation as the user can't see the total currency charged for the booking prior to booking...).

    Raises
    ------
    ValueError
        * If the user tries to book a number of rooms that exceeds the number of rooms available in the relevant hotel.
        * If the user passes another datatype than int for amount of night or rooms.
        * If the user specifies an int less than or equal to zero for nights or rooms.
        * If the user wishes to book a hotel that doesn't exist.
    Exception
        If the user cancels the booking.
    """
    try:
        nights = int(nights)  # Convert str to int. Int is required for calculations later.
        rooms = int(rooms)  # While float does work for calculations, it doesn't make sense to book a fraction of a room
    except ValueError:  # Catch error if datatype conversion doesn't work.
        raise ValueError("Nights and rooms must be integers.")

    if (nights or rooms) <= 0:  # A booking shouldn't be 'negative'. Otherwise, the user could earn money from booking.
        raise ValueError("Nights and rooms must be greater than 0.")

    hotel = next((item for item in hotels_data if hotel.lower() in item['name'].lower()), None)  # Find the hotel.

    if not hotel:
        raise ValueError("Hotel does not exist.")

    total_cost = nights * rooms * hotel['cost_per_room']  # Cost calculation

    if rooms > hotel['rooms_available']:
        raise ValueError('Not enough rooms available.')

    new_booking = create_booking_dict(user, hotel['name'], nights, rooms, total_cost)  # Create the booking dict.

    print(' ')
    for e in new_booking:
        print(f'{e.capitalize()}: {new_booking[e]}')
    print(' ')
    if confirmation.lower() == "n":
        raise Exception('Booking cancelled by user.')
    elif confirmation.lower() == "no":
        raise Exception('Booking cancelled by user.')  # Cancels the booking process.

    bookings_data.append(new_booking)  # Append the booking to the booking list.
    hotels_data[hotels_data.index(hotel)]['rooms_available'] -= rooms  # Mark the number of rooms booked as unavailable.

    if f_save:  # Some hypothetical testing environments would not want the function to save the data.
        save(bookings_data, hotels_data)

    print('Booking successfully created.')


def save(bookings_data, hotels_data):
    try:
        with open("bookings.json", "w") as file:  # 'w' clears the file from data.
            json.dump(bookings_data, file, indent=4)  # json.dump writes to the file with desired data.
        with open("hotels.json", "w") as file:
            json.dump(hotels_data, file, indent=4)  # Standard indentation is four spaces.
    except FileNotFoundError:
        raise FileNotFoundError("JSON file not found.")
    except json.JSONDecodeError:
        raise ValueError("File is not a valid JSON file.")


def display_bookings(bookings_data, show_index):
    """Prints the bookings provided in bookings_data to the terminal.
    Also shows the index of each booking if show_index is True.

    Parameters
    ----------
    bookings_data : list of dicts, mandatory
        The bookings to be printed to the terminal.
    show_index : boolean, mandatory
        show_index determines if the index of each booking in the database is to be printed or not.

    Raises
    ------
    ValueError
        Bookings data provided is invalid.
    """
    if is_invalid_data(bookings_data):  # Check for incompatibility.
        raise ValueError('An error occurred in the loading of bookings data. Invalid bookings data provided.')

    for item in bookings_data:  # For every booking.
        keys = list(item.keys())
        bookie = list(item.values())
        bookie_index = bookings_data.index(item)  # Index is grabbed here for possible use if show_index == True.

        for p in range(len(bookie)):
            if p == 0:
                print(f'{bookie[p]}')
            else:
                print(f'    {keys[p]}: {bookie[p]}')
        if show_index:  # show_index is needed when removing a booking.
            print(f'    index: {bookie_index}')


def print_command_list():
    print("These are the current commands available: \n")
    print("    * 'bookings' - Prints all bookings listed in the bookings file.")
    print("    * 'bookings index' - Prints all bookings listed in the bookings file, with the index of each booking in the file (useful for removing bookings).")
    print("    * 'hotels' - Prints all hotels listed in the hotels file.")
    print("    * 'sort' - Prints all hosted sorted by a certain property given by the user, ascending or descending in order.")
    print("    * 'create booking' - Useful for creating a booking.")
    print("    * 'remove booking' - Useful for removing a booking.")
    print("    * 'search by location' - Prints each hotel available at a certain location.")
    print("    * 'clear disable' - Disables command prompt clearing after each user input cycle.")
    print("    * 'clear enable' - Enables command prompt clearing after each user input cycle.")
    print("    * 'help' - Prints the command list.")


if __name__ == "__main__":
    print("BOOKING early build. Enter 'help' for help.")
    while True:
        data = get_data("hotels.json")  # Get the hotel dataset
        bookings = get_data("bookings.json")  # Get the booking dataset
        request = input(">> ").lower()  # Grab user input. .lower() insures we ignore capitalisation.
        clear(clear_enabled)  # Clear terminal if clear_enabled == True.

        try:
            match request:  # Every program response to user input is here.
                case "bookings":
                    display_bookings(bookings, False)
                case "bookings index":
                    display_bookings(bookings, True)
                case "hotels":
                    display_hotels(data)
                case "sort":
                    print("Properties available to be sorted by:\n'name', 'location', 'rooms_available', 'cost_per_room', rating'")
                    key = input('Sort by property: ')
                    order = input('Ascending/descending: ')

                    if order.lower() == 'ascending': order = False
                    else: order = True

                    data = sort_hotels(data, key, order)
                    display_hotels(data)
                case "remove booking":
                    remove_booking(data, bookings)
                case "create booking":
                    create_booking(data, bookings, True, user=input("Name: "), hotel=input("Hotel: "),
                           nights=input("Amount of nights: "), rooms=input("Number of rooms: "),
                           confirmation=input('Confirm booking? (yes/no): ').lower())
                case "search by location":
                    loc = input("Search for: ")
                    search_by_location(data, loc)
                case "clear disable":
                    clear_enabled = False
                case "clear enable":
                    clear_enabled = True
                case "help":
                    print_command_list()

        except Exception as e:
            print(f"Error: {e}")
