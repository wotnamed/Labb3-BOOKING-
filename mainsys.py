import json
import os
import pytest

def clear():
    os.system("cls")

def get_data():
    try:
        with open("hotels.json", "r") as file:
            hotel_list = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("hotels.json not found.")
    except json.JSONDecodeError:
        raise ValueError("hotels.json is not a valid JSON file.")

    return hotel_list

def get_bookings():
    try:
        with open("bookings.json", "r") as file:
            bookings_list = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("bookings.json not found.")
    except json.JSONDecodeError:
        raise ValueError("bookings.json is not a valid JSON file.")

    return bookings_list

def display_hotels(hotels_data):
    """ Prints each item in a list and each list's keys and respective values.
    The first key and value is printed in a 'rubrik-like' manner."""
    for h in hotels_data:
        keys = list(h.keys())
        hotel = list(h.values())

        for p in range(len(hotel)):
            if p == 0:
                print(f'{hotel[p]}')
            else:
                print(f'    {keys[p]}: {hotel[p]}')

def sort_hotels(hotels_data, k, reverse):
    def a(i):
        try:
            return i[k]
        except KeyError:
            pass

    hotels_data.sort(reverse=reverse, key=a)

    return hotels_data

def search_by_location(hotels_data, location):
    hotels = []

    try:
        hotels = list(filter(lambda hotels_data : hotels_data['location'].lower() == location.lower(), hotels_data))[0]
    except IndexError:
        raise ValueError('No hotel found.')

    for hotel in hotels:
        print(hotel)

    return hotels

def remove_booking(hotels_data, bookings_data):
    print("Choose a booking to be removed.")
    display_bookings(bookings_data, True)
    index_of_booking = int(input("Please provide the index of the booking to be removed: "))
    hotel = bookings_data[index_of_booking]["hotel"]
    print(hotel)
    rooms_of_booking = int(bookings_data[index_of_booking]["rooms booked"])
    try:
        hotel = list(filter(lambda hotels_data : hotels_data['name'].lower() == hotel.lower(), hotels_data))[0]
    except IndexError:
        raise ValueError('Hotel does not exist.')
    hotels_data[hotels_data.index(hotel)]['rooms_available'] += rooms_of_booking
    bookings_data.pop(index_of_booking)
    with open("bookings.json", "w") as file:
        json.dump(bookings_data, file, indent=4)
    with open("hotels.json", "w") as file:
        json.dump(hotels_data, file, indent=4)
    print("Booking successfully removed.")

def create_booking(hotels_data, bookings_data):
    user = input("Name: ")
    hotel = input("Hotel: ")

    try:
        nights = int(input("Amount of nights: "))
        rooms = int(input("Amount of rooms: "))
    except ValueError:
        raise ValueError("Nights and rooms must be integers.")

    if (nights or rooms) <= 0:
        raise ValueError("Nights and rooms must be greater than 0.")

    try:
        hotel = list(filter(lambda hotels_data : hotels_data['name'].lower() == hotel.lower(), hotels_data))[0]
    except IndexError:
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

    try:
        with open("bookings.json", "w") as file:
            json.dump(bookings_data, file, indent=4)

        with open("hotels.json", "w") as file:
            json.dump(hotels_data, file, indent=4)
    except FileNotFoundError:
        raise FileNotFoundError("JSON file not found.")
    except json.JSONDecodeError:
        raise ValueError("File is not a valid JSON file.")

    print('Booking successfully created.')

def display_bookings(bookings_data, show_index):
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

if __name__ == "__main__":
    while True:
        data = get_data()
        bookings = get_bookings()
        request = input()

        clear()

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
                    print('List cannot be sorted by that property.')
            elif request.lower() == "remove booking":
                remove_booking(data, bookings)
            elif request.lower() == "create booking":
                create_booking(data, bookings)
            elif request.lower() == "search by location":
                loc = input("Search for: ")
                search_by_location(data, loc)

        except Exception as e:
            print(f"Error: {e}")

#def test_sort_hotels():
#   assert sort_hotels(get_data(), "rating", "descending") == "a"