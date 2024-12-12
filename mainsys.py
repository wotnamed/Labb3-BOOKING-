import json

def get_data():
    # json.dumps(data) dump string not file
    # youtube tutorial https://www.youtube.com/watch?v=-51jxlQaxyA
    with open("hotels.json", "r") as e:
        hotel_list = json.load(e)

    return hotel_list

get_data()

#Hjewdå