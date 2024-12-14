from enum import Enum
from typing import Dict, Type

# Define your Enum
class AllowedKeys(Enum):
    NAME = "name"
    AGE = "age"
    CITY = "city"

# Your dictionary
my_dict = {
    "name": "Alice",
    "age": 30,
    "city": "New York",
    "country": "USA"  # Invalid key
}

# Check if all keys in the dictionary are in the Enum
def validate_keys(dict_obj: Dict[any, any], enum_class: Type[Enum]):
    # Get the set of valid keys from the Enum
    valid_keys = {e.value for e in enum_class}

    # Get the set of keys in the dictionary
    dict_keys = set(dict_obj.keys())

    # Check for invalid keys
    invalid_keys = dict_keys - valid_keys

    if invalid_keys:
        print(f"Invalid keys found: {invalid_keys}")
        return False

    print("All keys are valid.")
    return True

# Validate the dictionary
validate_keys(my_dict, AllowedKeys)
