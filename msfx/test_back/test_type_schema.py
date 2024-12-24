
from typing import Dict, Any

from msfx.lib_back2.util.generics import dict_validate, SCHEMA_TYPE

DATA_SCHEMA = {
    "name": {"type": str, "default": ""},
    "age": {"type": int, "default": -1},
    "source": {"type": list, "default": []}
}

def validate(data: Dict[str, Any], schema: dict) -> None:
    if not isinstance(data, dict):
        error = f"Data must be of type {dict}"
        raise ValueError(error)
    for key, info in schema.items():
        if key not in data:
            error = f"Missing key: {key} in data"
            raise KeyError(error)
        valid_type = info[SCHEMA_TYPE]
        if not isinstance(data[key], valid_type):
            error = f"Incorrect type for key: {key}. "
            error += f"Expected {valid_type.__name__}, "
            error += f"got {type(data[key]).__name__}."
            raise TypeError(error)



data_chk = {
    "name": "Roger",
    "age": 0.1
}
dict_validate(data_chk, DATA_SCHEMA)