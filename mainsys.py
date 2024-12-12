import json


def get_data():
    # json.dumps(data) dump string not file
    # youtube tutorial https://www.youtube.com/watch?v=-51jxlQaxyA
    with open("hotels.json", "r") as e:
        hotel_list = json.load(e)

    return hotel_list

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



while True:
    data = get_data()
    request = input()

    if request.lower() == "hotels":
        display_hotels(data)
    if request.lower() == "sort":
        key = input('Sort by property: ')
        order = input('Ascending/descending: ')

        if order.lower() == 'ascending': order = False
        else: order = True

        data = sort_hotels(data, key, order)
        display_hotels(data)
