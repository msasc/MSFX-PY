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
from typing import Any, Optional, Dict, List, Tuple, Union

def validate_dict(data: dict, master_keys: list | tuple, required_keys: list | tuple):
    """
    Validates that a given dictionary has no keys out of the master keys, and
    at least the required keys.
    :param data: The dictionary to validate.
    :param master_keys: The master keys. The dictionary can not have keys outside
    the master keys.
    :param required_keys: The required keys that the dictionay must at least contain.
    """

    # Check no keys outside the master keys.
    for key in data.keys():
        if key not in master_keys:
            raise KeyError("Key {} is not one of the master keys".format(key))

    # Check that the dictionary conatins at least the required keys.
    for key in required_keys:
        if key not in data:
            raise KeyError("Key {} is not one of the required keys".format(key))

"""
Helpers to get/put values from/to a dictionary checking that the value,
if contained in the dictionary, is of the proper type.

Theese functions are aimed to be used in objects that store its internal
data in a dictionary and the overload of validation is not significative.
"""

def get_bool(data: dict, key, default=False) -> bool:
    value = data.get(key, default)
    if isinstance(value, bool): return value
    raise TypeError("Key: {}, Value: {} is not bool".format(key, value))
def get_integer(data: dict, key, default=0) -> int:
    value = data.get(key, default)
    if isinstance(value, (int, float, Decimal)): return int(value)
    if isinstance(value, complex): return int(value.real)
    raise TypeError("Key: {}, Value: {} is not number".format(key, value))
def get_float(data: dict, key, default=0.0) -> float:
    value = data.get(key, default)
    if isinstance(value, (int, float, Decimal)): return float(value)
    if isinstance(value, complex): return float(value.real)
    raise TypeError("Key: {}, Value: {} is not number".format(key, value))
def get_decimal(data: dict, key, default=Decimal(0)) -> Decimal:
    value = data.get(key, default)
    if isinstance(value, (int, float, Decimal)): return Decimal(value)
    if isinstance(value, complex): return Decimal(value.real)
    raise TypeError("Key: {}, Value: {} is not number".format(key, value))
def get_complex(data: dict, key, default=complex(0, 0)) -> complex:
    value = data.get(key, default)
    if isinstance(value, (int, float, Decimal, complex)): return complex(value)
    raise TypeError("Key: {}, Value: {} is not number".format(key, value))
def get_string(data: dict, key, default="") -> str:
    value = data.get(key, default)
    if isinstance(value, str): return value
    raise TypeError("Key: {}, Value: {} is not string".format(key, value))
def get_date(data: dict, key, default=None) -> Optional[date]:
    value = data.get(key, default)
    if isinstance(value, date): return value
    if isinstance(value, datetime): return value.date()
    if value is None: return None
    raise TypeError("Key: {}, Value: {} is not date".format(key, value))
def get_time(data: dict, key, default=None) -> Optional[time]:
    value = data.get(key, default)
    if isinstance(value, time): return value
    if isinstance(value, datetime): return value.time()
    if value is None: return None
    raise TypeError("Key: {}, Value: {} is not time".format(key, value))
def get_datetime(data: dict, key, default=None) -> Optional[datetime]:
    value = data.get(key, default)
    if isinstance(value, datetime): return value
    if value is None: return None
    raise TypeError("Key: {}, Value: {} is not datetime".format(key, value))
def get_binary(data: dict, key, default=None) -> bytes or bytearray:
    value = data.get(key, default)
    if isinstance(value, (bytes, bytearray)): return value
    if value is None: return None
    raise TypeError("Key: {}, Value: {} is not binary".format(key, value))
def get_list(data: dict, key, default=None) -> list:
    value = data.get(key, default)
    if isinstance(value, list): return value
    if value is None: return []
    raise TypeError("Key: {}, Value: {} is not list".format(key, value))
def get_dict(data: dict, key, default=None) -> dict:
    value = data.get(key, default)
    if isinstance(value, dict): return value
    if value is None: return {}
    raise TypeError("Key: {}, Value: {} is not dict".format(key, value))
def get_any(data: dict, key, default=None) -> Any: return data.get(key, default)

def set_bool(data: dict, key, value: bool):
    if not isinstance(value, bool): raise TypeError("Value {} is not bool".format(value))
    data[key] = value
def set_integer(data: dict, key, value: int):
    if not isinstance(value, int): raise TypeError("Value {} is not integer".format(value))
    data[key] = value
def set_float(data: dict, key, value: float):
    if not isinstance(value, float): raise TypeError("Value {} is not float".format(value))
    data[key] = value
def set_complex(data: dict, key, value: complex):
    if not isinstance(value, complex): raise TypeError("Value {} is not complex".format(value))
    data[key] = value
def set_decimal(data: dict, key, value: Decimal):
    if not isinstance(value, Decimal): raise TypeError("Value {} is not decimal".format(value))
    data[key] = value
def set_string(data: dict, key, value: str):
    if not isinstance(value, str): raise TypeError("Value {} is not string".format(value))
    data[key] = value
def set_date(data: dict, key, value: date):
    if not isinstance(value, date): raise TypeError("Value {} is not date".format(value))
    data[key] = value
def set_time(data: dict, key, value: time):
    if not isinstance(value, time): raise TypeError("Value {} is not time".format(value))
    data[key] = value
def set_datetime(data: dict, key, value: datetime):
    if not isinstance(value, datetime): raise TypeError("Value {} is not datetime".format(value))
    data[key] = value
def set_binary(data: dict, key, value: (bytes, bytearray)):
    if not isinstance(value, (bytes, bytearray)): raise TypeError("Value {} is not binary".format(value))
    data[key] = value
def set_list(data: dict, key, value: list):
    if not isinstance(value, list): raise TypeError("Value {} is not list".format(value))
    data[key] = value
def set_tuple(data: dict, key, value: tuple):
    if not isinstance(value, tuple): raise TypeError("Value {} is not tuple".format(value))
    data[key] = value
def set_dict(data: dict, key, value: dict):
    if not isinstance(value, dict): raise TypeError("Value {} is not dict".format(value))
    data[key] = value
def set_any(data: dict, key, value: Any): data[key] = value
