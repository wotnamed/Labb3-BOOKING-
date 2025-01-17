import unittest
import json
import os
import pytest
from mainsys import *
import sys
from unittest.mock import patch
from io import StringIO
from test import *
display_hotels(test_hotels_dataset)
print("sasfasfasf")
def test_display_hotels():
    with (patch('sys.stdout', StringIO) as mock_stdout):
        display_hotels(test_hotels_dataset)
        actual_output = mock_stdout.getvalue().strip()
        expected_output = "Graze The Roof\n    location: Stockholm, Sweden\n    rooms_available: 23\n    cost_per_room: 399\n    rating: 4.5\n\nTesting Besting\n    location: Gothenburg, Sweden\n    rooms_available: 4\n    cost_per_room: 500\n    rating: 4.9\n\nGraze The Roof\n    location: Stockholm, Sweden\n    rooms_available: 23\n    cost_per_room: 399\n    rating: 4.5\n\nTesting Besting\n    location: Gothenburg, Sweden\n    rooms_available: 4\n    cost_per_room: 500\n    rating: 4.9\n"
        assert actual_output == expected_output
   # assert display_hotels(test_hotels_dataset) == "Graze The Roof\n    location: Stockholm, Sweden\n    rooms_available: 23\n    cost_per_room: 399\n    rating: 4.5\n\nTesting Besting\n    location: Gothenburg, Sweden\n    rooms_available: 4\n    cost_per_room: 500\n    rating: 4.9\n\nGraze The Roof\n    location: Stockholm, Sweden\n    rooms_available: 23\n    cost_per_room: 399\n    rating: 4.5\n\nTesting Besting\n    location: Gothenburg, Sweden\n    rooms_available: 4\n    cost_per_room: 500\n    rating: 4.9\n"

