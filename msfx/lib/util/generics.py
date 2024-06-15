#  Copyright (c) 2024 Miquel Sas.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

""" Utility functions for dictionaries """
from typing import Any, Type, Dict

def dict_create(schema: Dict[str, Any]) -> Dict[str, Any]:
    return {key: value for key, value in schema.items()}

def dict_get_value(data: dict, key: str, schema: Dict[str, Any]) -> Any:
    if not isinstance(data, dict):
        error = f"Data must be of type {dict}"
        raise ValueError(error)
    if not key in schema:
        error = f"Key must be in the schema"
        raise KeyError(error)
    return data.get(key, schema[key])

def dict_set_value(data: dict, key: str, value: Any, expected_type: Type[Any]):
    if not isinstance(value, expected_type):
        error = f"value must be of type {expected_type.__name__}"
        raise ValueError(error)
    data[key] = value

def dict_validate(data: Dict[str, Any], schema: Dict[str, Any], admit_empty=False) -> None:
    if not isinstance(data, dict):
        error = f"Data must be of type {dict}"
        raise ValueError(error)
    if admit_empty and len(data) == 0:
        return
    if not admit_empty and len(data) == 0:
        error = f"Data can not be empty."
        raise ValueError(error)
    for key, expected_value in schema.items():
        if key not in data:
            error = f"Missing key: {key} in data"
            raise KeyError(error)
        if not isinstance(data[key], type(expected_value)):
            error = f"Incorrect type for key: {key}. "
            error += f"Expected {type(expected_value).__name__}, "
            error += f"got {type(data[key]).__name__}."
            raise TypeError(error)
