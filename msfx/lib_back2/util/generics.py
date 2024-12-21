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

SCHEMA_TYPE = "type"
SCHEMA_DEFAULT = "default"

def dict_create_default(schema: dict) -> dict:
    default_data = {}
    for key, value in schema.items():
        schema_type = value[SCHEMA_TYPE]
        if schema_type in {list, dict}:
            default_data[key] = schema_type()
        else:
            default_data[key] = value[SCHEMA_DEFAULT]
    return default_data

def dict_create_args(schema: dict, **kwargs) -> dict:
    default_data = {}
    for key, value in schema.items():
        schema_type = value[SCHEMA_TYPE]
        if key in kwargs:
            value = kwargs[key]
            if not isinstance(value, schema_type):
                error = f"Incorrect type for key in kwargs: {key}. "
                error += f"Expected {type(schema_type).__name__}, "
                error += f"got {type(value).__name__}."
                raise TypeError(error)
            default_data[key] = value
    return default_data

def dict_get_value(data: dict, key: str, schema: dict) -> Any:
    if not isinstance(data, dict):
        error = f"Data must be of type {dict}"
        raise ValueError(error)
    if not key in schema:
        error = f"Key must be in the schema"
        raise KeyError(error)
    return data.get(key, schema[key][SCHEMA_DEFAULT])

def dict_set_value(data: dict, key: str, value: Any, expected_type: Type[Any]):
    if not isinstance(value, expected_type):
        error = f"value must be of type {expected_type.__name__}"
        raise ValueError(error)
    data[key] = value

def dict_validate(data: dict, schema: dict, empty=False) -> None:
    if not isinstance(data, dict):
        error = f"Data must be of type {dict}"
        raise ValueError(error)
    if not empty and len(data) == 0:
        error = f"Data can not be empty"
        raise ValueError(error)
    if empty and len(data) == 0:
        return
    for key, schema_info in schema.items():
        if key not in data:
            error = f"Missing key: {key} in data"
            raise KeyError(error)
        schema_type = schema_info[SCHEMA_TYPE]
        if not isinstance(data[key], schema_type):
            error = f"Incorrect type for key: {key}. "
            error += f"Expected {type(schema_type).__name__}, "
            error += f"got {type(data[key]).__name__}."
            raise TypeError(error)
