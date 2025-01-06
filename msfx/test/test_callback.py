from typing import Callable

# Define a function that accepts a callback
def process_string(value: str, callback: Callable[[str], int]) -> int:
    result = callback(value)
    return result

# Define a callback function that matches the signature
def string_length(s: str) -> int:
    return len(s)

# Using the function
print(process_string("Hello, world!", string_length))  # Output: 13
