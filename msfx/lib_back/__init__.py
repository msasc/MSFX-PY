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

from datetime import datetime, time, date
from decimal import Decimal
from enum import Enum
from typing import Any, Optional, Dict, Type

def __err_quote__(value) -> str:
    err: str = ""
    if isinstance(value, str): err += "\""
    err += "{}"
    if isinstance(value, str): err += "\""
    return err

def __err_get__(key, value, expected) -> str:
    err: str = "The pair \"{}\"/" + __err_quote__(value) + " is included in the dictionary but is not a {}"
    return err.format(key, value, expected)

def __err_put__(value, expected) -> str:
    return ("The value " + __err_quote__(value) + " must be a {}").format(value, expected)

def __err_key__(key) -> str:
    return "The key {} must be a string".format(key)

"""
Helpers to get/put values from/to a dictionary checking that the value,
if contained in the dictionary, is of the proper type.

Theese functions are aimed to be used in objects that store its internal
data in a dictionary and the overload of validation is not significative. 
"""

def get_bool(data: dict, key, default=False) -> bool:
    value = data.get(key, default)
    if isinstance(value, bool): return value
    raise TypeError(__err_get__(key, value, "boolean"))

def get_integer(data: dict, key, default=0) -> int:
    value = data.get(key, default)
    if isinstance(value, (int, float, Decimal)): return int(value)
    if isinstance(value, complex): return int(value.real)
    raise TypeError(__err_get__(key, value, "number"))

def get_float(data: dict, key, default=0.0) -> float:
    value = data.get(key, default)
    if isinstance(value, (int, float, Decimal)): return float(value)
    if isinstance(value, complex): return float(value.real)
    raise TypeError(__err_get__(key, value, "number"))

def get_decimal(data: dict, key, default=Decimal(0)) -> Decimal:
    value = data.get(key, default)
    if isinstance(value, (int, float, Decimal)): return Decimal(value)
    if isinstance(value, complex): return Decimal(value.real)
    raise TypeError(__err_get__(key, value, "number"))

def get_complex(data: dict, key, default=complex(0, 0)) -> complex:
    value = data.get(key, default)
    if isinstance(value, (int, float, Decimal, complex)): return complex(value)
    raise TypeError(__err_get__(key, value, "number"))

def get_string(data: dict, key, default="") -> str:
    value = data.get(key, default)
    if isinstance(value, str): return value
    raise TypeError(__err_get__(key, value, "string"))

def get_date(data: dict, key, default=None) -> Optional[date]:
    value = data.get(key, default)
    if isinstance(value, date): return value
    if isinstance(value, datetime): return value.date()
    if value is None: return None
    raise TypeError(__err_get__(key, value, "date or datetime"))

def get_time(data: dict, key, default=None) -> Optional[time]:
    value = data.get(key, default)
    if isinstance(value, time): return value
    if isinstance(value, datetime): return value.time()
    if value is None: return None
    raise TypeError(__err_get__(key, value, "time or datetime"))

def get_datetime(data: dict, key, default=None) -> Optional[datetime]:
    value = data.get(key, default)
    if isinstance(value, datetime): return value
    if value is None: return None
    raise TypeError(__err_get__(key, value, "datetime"))

def get_binary(data: dict, key, default=None) -> bytes or bytearray:
    value = data.get(key, default)
    if isinstance(value, (bytes, bytearray)): return value
    if value is None: return None
    raise TypeError(__err_get__(key, value, "binary"))

def get_list(data: dict, key, default=None) -> list:
    value = data.get(key, default)
    if isinstance(value, list): return value
    if value is None: return []
    raise TypeError(__err_get__(key, value, "list"))

def get_dict(data: dict, key, default=None) -> dict:
    value = data.get(key, default)
    if isinstance(value, dict): return value
    if value is None: return {}
    raise TypeError(__err_get__(key, value, "dictionary"))

def get_any(data: dict, key, default=None) -> Any: return data.get(key, default)

def put_bool(data: dict, key, value: bool):
    if not isinstance(value, bool): raise TypeError(__err_put__(value, "boolean"))
    data[key] = value

def put_integer(data: dict, key, value: int):
    if not isinstance(value, int): raise TypeError(__err_put__(value, "integer"))
    data[key] = value

def put_float(data: dict, key, value: float):
    if not isinstance(value, float): raise TypeError(__err_put__(value, "float"))
    data[key] = value

def put_complex(data: dict, key, value: complex):
    if not isinstance(value, complex): raise TypeError(__err_put__(value, "complex"))
    data[key] = value

def put_decimal(data: dict, key, value: Decimal):
    if not isinstance(value, Decimal): raise TypeError(__err_put__(value, "decimal"))
    data[key] = value

def put_string(data: dict, key, value: str):
    if not isinstance(value, str): raise TypeError(__err_put__(value, "string"))
    data[key] = value

def put_date(data: dict, key, value: date):
    if not isinstance(value, date): raise TypeError(__err_put__(value, "date"))
    data[key] = value

def put_time(data: dict, key, value: time):
    if not isinstance(value, time): raise TypeError(__err_put__(value, "time"))
    data[key] = value

def put_datetime(data: dict, key, value: datetime):
    if not isinstance(value, datetime): raise TypeError(__err_put__(value, "datetime"))
    data[key] = value

def put_binary(data: dict, key, value: (bytes, bytearray)):
    if not isinstance(value, (bytes, bytearray)): raise TypeError(__err_put__(value, "binary"))
    data[key] = value

def put_list(data: dict, key, value: list):
    if not isinstance(value, list): raise TypeError(__err_put__(value, "list"))
    data[key] = value

def put_dict(data: dict, key, value: dict):
    if not isinstance(value, dict): raise TypeError(__err_put__(value, "dictionary"))
    data[key] = value

def put_any(data: dict, key, value: Any): data[key] = value

def validate_enum_keys(data: Dict[any, any], enum_class: Type[Enum], error: str):
    valid_keys: set = {e.value for e in enum_class}
    dict_keys = set(data.keys())
    invalid_keys: set = dict_keys - valid_keys
    if invalid_keys: raise TypeError("Data is not {} data".format(error))
