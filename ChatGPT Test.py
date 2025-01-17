import sys
from io import StringIO


def my_function():
    print("Hello, world!")
    # You can have more print statements or other operations here


def test_my_function():
    # Redirect stdout to an in-memory buffer
    output_buffer = StringIO()
 = output_buffer

    # Call the function
    my_function()

    # Reset stdout
    sys.stdout = sys.__stdout__

    # Get the captured output
    printed_output = output_buffer.getvalue()

    # Now you can assert or check the output as needed
    expected_output = "Hello, world!\n"  # Include newline as print adds it

    assert printed_output == expected_output
    print("Test passed!")


# Run the test
test_my_function()