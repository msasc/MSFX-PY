from typing import Dict, Any, Union

from msfx.lib.db.types import Types

# Example schema with default values
COLUMN_KEYS: Dict[str, Union[str, Types, int, bool]] = {
    "name": "",
    "alias": "",
    "type": Types.NONE,
    "length": -1,
    "decimals": -1,
    "primary_key": False,
    "header": "",
    "label": "",
    "decription": ""  # Assuming this is intended to be "description"
}

def validate_data(data: Dict[str, Any], schema: Dict[str, Any]) -> None:
    for key, expected_value in schema.items():
        if key not in data:
            raise KeyError(f"Missing key: {key} in data")
        if not isinstance(data[key], type(expected_value)):
            raise TypeError(
                f"Incorrect type for key: {key}. Expected {type(expected_value).__name__}, "
                f"got {type(data[key]).__name__}."
            )

# Example usage
valid_data = {
    "name": "Column1",
    "alias": "col1",
    "type": Types.NONE,
    "length": 10,
    "decimals": 2,
    "primary_key": True,
    "header": "Header1",
    "label": "Label1",
    "decription": "Description1"
}

invalid_data = {
    "name": "Column1",
    "alias": "col1",
    "type": Types.NONE,
    "length": "ten",  # Invalid type
    "decimals": 2,
    "primary_key": True,
    "header": "Header1",
    "label": "Label1",
    "decription": "Description1"
}

try:
    validate_data(valid_data, COLUMN_KEYS)
    print("Valid data passed validation.")
except (KeyError, TypeError) as e:
    print(e)

try:
    validate_data(invalid_data, COLUMN_KEYS)
except (KeyError, TypeError) as e:
    print(e)  # Should print an error message about the incorrect type for "length"

SCHEMA = {
    "columns": [],
    "indexes": {}
}