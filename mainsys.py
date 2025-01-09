import json
import os
import pytest

#  running parameters
clear_enabled = False


def clear(status):
    if status:
        os.system("cls||clear")


def get_data():
    """Loads the hotels data from 'hotels.json'.

            Parameters
            ----------
            None

            Return
            ------
            hotel_list : list of dicts
                The JSON data loaded into a list.

            Raises
            ------
            FileNotFoundError
                If the JSON file was not found.
            ValueError
                If the file was not a valid JSON file.
            """
    try:
        with open("hotels.json", "r") as file:
            hotel_list = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("hotels.json not found.")
    except json.JSONDecodeError:
        raise ValueError("hotels.json is not a valid JSON file.")

    return hotel_list


def get_bookings():
    """Loads the bookings data from 'bookings.json'.

                Parameters
                ----------
                None

                Return
                ------
                bookings_list : list of dicts
                    The JSON data loaded into a list.

                Raises
                ------
                FileNotFoundError
                    If the JSON file was not found.
                ValueError
                    If the file was not a valid JSON file.
                """
    try:
        with open("bookings.json", "r") as file:
            bookings_list = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("bookings.json not found.")
    except json.JSONDecodeError:
        raise ValueError("bookings.json is not a valid JSON file.")

    return bookings_list


def display_hotels(hotels_data):
    """ Prints every hotel and its data.

    The hotel name is printed in a rubric-like manner, as the data for each hotel is indented under the name.

    Parameters
    ----------
    hotels_data : list, mandatory
        The list of hotels, in which each hotel is a dictionary with key:value pairs.

    Raises
    ------
    None
    """
    for h in hotels_data:
        keys = list(h.keys())
        hotel = list(h.values())

        for p in range(len(hotel)):
            if p == 0:
                print(f'{hotel[p]}')
            else:
                print(f'    {keys[p]}: {hotel[p]}')
        print()


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

        Return
        ------
        hotels_data : list of dicts
            The sorted 'hotels' dataset.

        Raises
        ------
        None
        """
    def a(i):
        try:
            return i[k]
        except KeyError:
            pass

    hotels_data.sort(reverse=reverse, key=a)

    return hotels_data


def search_by_location(hotels_data, location):
    try:
        hotels = list(filter(lambda hotels_data : hotels_data['location'].lower() == location.lower(), hotels_data))
        for i in hotels:
            keys = list(i.keys())
            hotel = list(i.values())

            for p in range(len(hotel)):
                if p == 0:
                    print(f'{hotel[p]}')
                else:
                    print(f'    {keys[p]}: {hotel[p]}')
            print()
    except IndexError:
        raise ValueError('No hotel found. (IndexError)') #  TODO: IDENTIFY IF INDEXERROR HANDLING IS NEEDED.
    if not hotels:
        raise ValueError('No hotel found.')


def remove_booking(hotels_data, bookings_data):
    """Removes a booking specified by the user in bookings_data, by index of the booking in the list.

    Also corrects for the recovered rooms in the hotels_data database.

    Parameters
    ----------
    hotels_data : list of dicts, mandatory
        The hotels database
    bookings_data . list of dicts, mandatory
        The bookings database

    Raises
    ------
    ValueError
        The hotel found in the booking is not present in the hotel database.
    """
    print("Choose a booking to be removed.")
    display_bookings(bookings_data, True)
    index_of_booking = int(input("Please provide the index of the booking to be removed: "))
    hotel = bookings_data[index_of_booking]["hotel"]
    rooms_of_booking = int(bookings_data[index_of_booking]["rooms booked"])

    try:
        hotel = list(filter(lambda hotels_data : hotels_data['name'].lower() == hotel.lower(), hotels_data))[0]
    except IndexError:
        raise ValueError('Hotel does not exist.')

    hotels_data[hotels_data.index(hotel)]['rooms_available'] += rooms_of_booking
    bookings_data.pop(index_of_booking)
    save(bookings_data, hotels_data)
    print("Booking successfully removed.")


def create_booking(hotels_data, bookings_data):
    """Creates a booking in the bookings_data database.

    Also adjusts the number of available rooms in the hotel_data database for the hotel booked by the user.

    The details of the booking is provided via the user in the terminal.

    Parameters
    ----------
    hotels_data : list of dicts, mandatory
        The hotel database
    bookings_data : list of dicts, mandatory
        The bookings database

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
    user = input("Name: ")
    hotel = input("Hotel: ")

    try:
        nights = int(input("Amount of nights: "))
        rooms = int(input("Amount of rooms: "))
    except ValueError:
        raise ValueError("Nights and rooms must be integers.")

    if (nights or rooms) <= 0:
        raise ValueError("Nights and rooms must be greater than 0.")

    hotel = next((item for item in hotels_data if hotel.lower() in item['name'].lower()), None)
    #hotel = list(filter(lambda hotels_data : hotels_data['name'].lower() == hotel.lower(), hotels_data))[0]
    if not hotel:
        raise ValueError("Hotel does not exist.")

    total_cost = nights * rooms * hotel['cost_per_room']

    if rooms > hotel['rooms_available']:
        raise ValueError('Not enough rooms available.')

    new_booking = {
        "booking name": user,
        "hotel": hotel['name'],
        "nights booked": nights,
        "rooms booked": rooms,
        "total cost": total_cost
    }

    print(' ')
    for e in new_booking:
        print(f'{e.capitalize()}: {new_booking[e]}')
    print(' ')
    confirmation = input('Confirm booking? (yes/no): ')
    if confirmation.lower() == ("no" or "n"):
        raise Exception('Booking cancelled by user.')

    bookings_data.append(new_booking)
    hotels_data[hotels_data.index(hotel)]['rooms_available'] -= rooms

    save(bookings_data, hotels_data)

    print('Booking successfully created.')


def save(bookings_data, hotels_data):
    try:
        with open("bookings.json", "w") as file:
            json.dump(bookings_data, file, indent=4)
        with open("hotels.json", "w") as file:
            json.dump(hotels_data, file, indent=4)
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
        No data to be printed has been provided.
    """
    if not bookings_data:
        raise ValueError("No bookings to display.")

    for bobject in bookings_data:
        keys = list(bobject.keys())
        bookie = list(bobject.values())
        bookie_index = bookings_data.index(bobject)

        for p in range(len(bookie)):
            if p == 0:
                print(f'{bookie[p]}')
            else:
                print(f'    {keys[p]}: {bookie[p]}')
        if show_index:
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
        data = get_data()
        bookings = get_bookings()
        request = input(">> ")
        clear(clear_enabled)

        try:
            if request.lower() == "bookings":
                display_bookings(bookings, False)
            elif request.lower() == "bookings index":
                display_bookings(bookings, True)
            elif request.lower() == "hotels":
                display_hotels(data)
            elif request.lower() == "sort":
                key = input('Sort by property: ')
                order = input('Ascending/descending: ')

                if order.lower() == 'ascending': order = False
                else: order = True

                try:
                    data = sort_hotels(data, key, order)
                    display_hotels(data)
                except TypeError:
                    raise TypeError("List cannot be sorted by that property.")
            elif request.lower() == "remove booking":
                remove_booking(data, bookings)
            elif request.lower() == "create booking":
                create_booking(data, bookings)
            elif request.lower() == "search by location":
                loc = input("Search for: ")
                search_by_location(data, loc)
            elif request.lower() == "clear disable":
                clear_enabled = False
            elif request.lower() == "clear enable":
                clear_enabled = True
            elif request.lower() == "help":
                print_command_list()

        except Exception as e:
            print(f"Error: {e}")


#  TESTING DATASETS: FOR TESTING ONLY:
test_hotels_dataset = [
    {
        "name": "Graze The Roof",
        "location": "Stockholm, Sweden",
        "rooms_available": 23,
        "cost_per_room": 399,
        "rating": 4.5
    },
    {
        "name": "Testing Besting",
        "location": "Gothenburg, Sweden",
        "rooms_available": 4,
        "cost_per_room": 500,
        "rating": 4.9
    }
]
test_bookings_dataset = [
    {
        "booking name": "mamam",
        "hotel": "Graze The Roof",
        "nights booked": 9,
        "rooms booked": 3,
        "total cost": 10773
    }
]
def test_sort_hotels():
   assert sort_hotels(test_hotels_dataset, "rating", True) == [
        {
            "name": "Testing Besting",
            "location": "Gothenburg, Sweden",
            "rooms_available": 4,
            "cost_per_room": 500,
            "rating": 4.9
        },
        {
            "name": "Graze The Roof",
            "location": "Stockholm, Sweden",
            "rooms_available": 23,
            "cost_per_room": 399,
            "rating": 4.5
        }
    ]
   #with pytest.raises(ValueError):
   #    sort_hotels("sawdusting", True)
#def test_display_hotels():
    #assert display_hotels(test_hotels_dataset) ==

