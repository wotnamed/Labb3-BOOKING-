import json

def get_data():
    with open("hotels.json", "r") as e:
        hotel_list = json.load(e)

    return hotel_list

def get_bookings():
    with open("bookings.json", "r") as file:
        bookings_list = json.load(file)

    return bookings_list

def display_hotels(hotels_data):
    for h in hotels_data:
        keys = list(h.keys())
        hotel = list(h.values())

        for p in range(len(hotel)):
            if p == 0:
                print(f'{hotel[p]}')
            else:
                print(f'    {keys[p]}: {hotel[p]}')

def sort_hotels(hotels_data, k, reverse):
    def a(e):
        return e[k]

    hotels_data.sort(reverse=reverse, key=a)

    return hotels_data

def search_by_location(hotels_data, location):
    hotels = []

    try:
        hotels = list(filter(lambda hotels_data : hotels_data['location'].lower() == location.lower(), hotels_data))[0]
    except IndexError:
        return print('No hotel found.')

    for hotel in hotels:
        print(hotel)

    return hotels

def create_booking(hotels_data, bookings_data):
    user = input("Name: ")
    hotel = input("Hotel: ")
    nights = int(input("Amount of nights: "))
    rooms = int(input("Amount of rooms: "))

    try:
        hotel = list(filter(lambda hotels_data : hotels_data['name'].lower() == hotel.lower(), hotels_data))[0]
    except IndexError:
        return print('Hotel does not exist.')

    total_cost = nights * rooms * hotel['cost_per_room']

    if rooms > hotel['rooms_available']:
        return print('Not enough rooms available.')

    if (nights or rooms) == 0:
        return print('You cannot book 0 nights or rooms.')

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
        return print('Cancelled booking.')

    bookings_data.append(new_booking)

    hotels_data[hotels_data.index(hotel)]['rooms_available'] -= rooms

    with open("bookings.json", "w") as file:
        json.dump(bookings_data, file, indent=4)

    with open("hotels.json", "w") as file:
        json.dump(hotels_data, file, indent=4)

    print('Booking successfully created.')

def display_bookings(bookings_data):
    if len(bookings_data) == 0: return print('No bookings to display.')
    print("The following is the documented bookings, yes?")
    for bobject in bookings_data:
        keys = list(bobject.keys())
        bookie = list(bobject.values())

        for p in range(len(bookie)):
            if p == 0:
                print(f'{bookie[p]}')
            else:
                print(f'    {keys[p]}: {bookie[p]}')

while True:
    data = get_data()
    bookings = get_bookings()
    request = input()
    if request.lower() == "bookings":
        display_bookings(bookings)
    elif request.lower() == "hotels":
        display_hotels(data)
    elif request.lower() == "sort":
        key = input('Sort by property: ')
        order = input('Ascending/descending: ')

        if order.lower() == 'ascending': order = False
        else: order = True

        data = sort_hotels(data, key, order)
        display_hotels(data)
    elif request.lower() == "create booking":
        create_booking(data, bookings)
    elif request.lower() == "search by location":
        loc = input("Search for: ")
        search_by_location(data, loc)
