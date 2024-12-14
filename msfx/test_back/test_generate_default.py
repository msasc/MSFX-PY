from typing import Any, Dict, List, Type

# Define the schema
DATA_SCHEMA = {
    "name": {"type": str, "default": ""},
    "age": {"type": int, "default": -1},
    "source": {"type": list, "default": []}
}

def generate_default_data(schema: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    default_data = {}
    for key, value in schema.items():
        # Use the type to generate new instances for mutable types
        if value["type"] in {list, dict}:
            default_data[key] = value["type"]()
        else:
            default_data[key] = value["default"]
    return default_data

def validate_data(data: Dict[str, Any], schema: Dict[str, Dict[str, Any]]) -> None:
    for key, value in schema.items():
        expected_type = value["type"]
        if key not in data:
            raise KeyError(f"Missing key: {key} in data")
        if not isinstance(data[key], expected_type):
            raise TypeError(
                f"Incorrect type for key: {key}. Expected {expected_type.__name__}, "
                f"got {type(data[key]).__name__}."
            )

# Example usage
default_data = generate_default_data(DATA_SCHEMA)
print(default_data)  # Should print: {'name': '', 'age': -1, 'source': []}

valid_data = {
    "name": "John",
    "age": 30,
    "source": ["source1", "source2"]
}

invalid_data = {
    "name": "John",
    "age": "thirty",  # Invalid type for age
    "source": ["source1", 2]  # Invalid type in source list
}

try:
    validate_data(valid_data, DATA_SCHEMA)
    print("Valid data passed validation.")
except (KeyError, TypeError) as e:
    print(e)

try:
    validate_data(invalid_data, DATA_SCHEMA)
except (KeyError, TypeError) as e:
    print(e)  # Should print an error message about the incorrect types
