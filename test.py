import unittest
import json
import os
import pytest
from mainsys import *
from unittest.mock import patch

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
   with pytest.raises(ValueError):
       sort_hotels(test_hotels_dataset, "saiodjauwdi", True)

def test_create_booking():
    create_booking(test_hotels_dataset, test_bookings_dataset, False, 'Causality', 'Graze The Roof', 2, 3, "y")
    assert test_bookings_dataset == [
        {
            "booking name": "mamam",
            "hotel": "Graze The Roof",
            "nights booked": 9,
            "rooms booked": 3,
            "total cost": 10773
        },
        {
            "booking name": "Causality",
            "hotel": "Graze The Roof",
            "nights booked": 2,
            "rooms booked": 3,
            "total cost": 2394
        }
    ]
    with pytest.raises(ValueError):
        create_booking(test_hotels_dataset, test_bookings_dataset, False, 'ffffgggg', '0', 2, 3, 'y')
    with pytest.raises(ValueError):
        create_booking(test_hotels_dataset, test_bookings_dataset, False, 'skrrrrkrkr', 'Graze The Roof', -1, 3, 'y')
    with pytest.raises(ValueError):
        create_booking(test_hotels_dataset, test_bookings_dataset, False, 'Causality', 'Graze The Roof', 2, 9999, 'y')
    with pytest.raises(Exception):
        create_booking(test_hotels_dataset, test_bookings_dataset, False, 'Causality', 'Graze The Roof', 2, 3, 'n')
    with pytest.raises(Exception):
        create_booking(test_hotels_dataset, test_bookings_dataset, False, 'Causality', 'Graze The Roof', 2, 3, 'no')

def test_display_hotels(capsys):
    display_hotels(test_hotels_dataset)

    captured = capsys.readouterr()

    assert captured.out == "Testing Besting\n    location: Gothenburg, Sweden\n    rooms_available: 4\n    cost_per_room: 500\n    rating: 4.9\n\nGraze The Roof\n    location: Stockholm, Sweden\n    rooms_available: 20\n    cost_per_room: 399\n    rating: 4.5\n\n"

    with pytest.raises(ValueError):
        display_hotels('')
    with pytest.raises(ValueError):
        display_hotels([])
    with pytest.raises(ValueError):
        display_hotels([{"aisdjw"}])

def test_search_by_location(capsys):
    hotels_data = get_data('hotels.json')

    search_by_location(hotels_data, 'Columbus')

    captured = capsys.readouterr()

    assert captured.out == "Hotel Sigma\n    location: Columbus, Ohio, USA\n    rooms_available: 420\n    cost_per_room: 69\n    rating: 5.0\n"

    with pytest.raises(ValueError):
        search_by_location(hotels_data, 'asiudghwi')
