import unittest
import json
import os
import pytest
from mainsys import *


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



