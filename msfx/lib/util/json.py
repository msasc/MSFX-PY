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

"""
JSON utilities.
"""

import decimal
import json
from datetime import date, time, datetime
from decimal import Decimal

def __serializer(obj):
    if isinstance(obj, date) and not isinstance(obj, datetime):
        return {"_date_": obj.isoformat()}
    elif isinstance(obj, time):
        return {"_time_": obj.isoformat()}
    elif isinstance(obj, datetime):
        return {"_datetime_": obj.isoformat()}
    elif isinstance(obj, Decimal):
        return {"_dec_": str(obj)}
    elif isinstance(obj, (bytes, bytearray)):
        return {"_bin_": obj.hex()}
    raise TypeError(f"Type {type(obj)} not serializable")

def __deserializer(dct):
    if "_date_" in dct:
        return date.fromisoformat(dct["_date_"])
    elif "_time_" in dct:
        return time.fromisoformat(dct["_time_"])
    elif "_datetime_" in dct:
        return datetime.fromisoformat(dct["_datetime_"])
    elif "_dec_" in dct:
        return Decimal(dct["_dec_"])
    elif "_bin_" in dct:
        return bytes.fromhex(dct["_bin_"])
    return dct

def loads(json_data) -> dict:
    return json.loads(json_data, object_hook=__deserializer)

def dumps(dct: dict, **kwargs) -> str:
    return json.dumps(dct, default=__serializer, **kwargs)

def get_bool(dct: dict, key: str) -> bool:
    value = dct.get(key)
    if isinstance(value, bool): return value
    raise TypeError(f"pair key {key} / value {value} is not a boolean")

def get_integer(dct: dict, key: str) -> int:
    value = dct.get(key)
    if isinstance(value, (int, float, Decimal)): return int(value)
    if isinstance(value, complex): return int(value.real)
    raise TypeError(f"pair key {key} / value {value} is not a number")

def get_float(dct: dict, key: str) -> float:
    value = dct.get(key)
    if isinstance(value, (int, float, Decimal)): return float(value)
    if isinstance(value, complex): return float(value.real)
    raise TypeError(f"pair key {key} / value {value} is not a number")

def get_decimal(dct: dict, key: str) -> decimal:
    value = dct.get(key)
    if isinstance(value, (int, float, Decimal)): return Decimal(value)
    if isinstance(value, complex): return Decimal(value.real)
    raise TypeError(f"pair key {key} / value {value} is not a number")

def get_string(dct: dict, key: str) -> str:
    value = dct.get(key)
    if isinstance(value, str): return value
    raise TypeError(f"pair key {key} / value {value} is not a string")

def get_date(dct: dict, key: str) -> date:
    value = dct.get(key)
    if isinstance(value, date): return value
    if isinstance(value, datetime): return value.date()
    raise TypeError(f"pair key {key} / value {value} is not a date or datetime")

def get_time(dct: dict, key: str) -> time:
    value = dct.get(key)
    if isinstance(value, time): return value
    if isinstance(value, datetime): return value.time()
    raise TypeError(f"pair key {key} / value {value} is not a time or datetime")

def get_binary(dct: dict, key: str) -> bytes or bytearray:
    value = dct.get(key)
    if isinstance(value, (bytes, bytearray)): return value
    raise TypeError(f"pair key {key} / value {value} is not a binary")

def get_tuple(dct: dict, key: str) -> tuple:
    value = dct.get(key)
    if isinstance(value, tuple): return value
    raise TypeError(f"pair key {key} / value {value} is not a tuple")

def get_list(dct: dict, key: str) -> list:
    value = dct.get(key)
    if isinstance(value, list): return value
    raise TypeError(f"pair key {key} / value {value} is not a list")

def get_dict(dct: dict, key: str) -> dict:
    value = dct.get(key)
    if isinstance(value, dict): return value
    raise TypeError(f"pair key {key} / value {value} is not a dictionary")

def put_bool(dct: dict, key: str, value: bool):
    if not isinstance(value, bool): raise TypeError("Value must be a boolean")
    dct[key] = value

def put_integer(dct: dict, key: str, value: int):
    if not isinstance(value, int): raise TypeError("Value must be an integer")
    dct[key] = value

def put_float(dct: dict, key: str, value: float):
    if not isinstance(value, float): raise TypeError("Value must be a float")
    dct[key] = value

def put_complex(dct: dict, key: str, value: complex):
    if not isinstance(value, complex): raise TypeError("Value must be a complex")
    dct[key] = value

def put_decimal(dct: dict, key: str, value: Decimal):
    if not isinstance(value, Decimal): raise TypeError("Value must be a decimal")
    dct[key] = value

def put_string(dct: dict, key: str, value: str):
    if not isinstance(value, str): raise TypeError("Value must be a string")
    dct[key] = value

def put_date(dct: dict, key: str, value: date):
    if not isinstance(value, date): raise TypeError("Value must be a date")
    dct[key] = value

def put_time(dct: dict, key: str, value: time):
    if not isinstance(value, time): raise TypeError("Value must be a time")
    dct[key] = value

def put_datetime(dct: dict, key: str, value: datetime):
    if not isinstance(value, datetime): raise TypeError("Value must be a datetime")
    dct[key] = value

def put_binary(dct: dict, key: str, value: (bytes, bytearray)):
    if not isinstance(value, (bytes, bytearray)): raise TypeError("Value must be a binary")
    dct[key] = value

def put_list(dct: dict, key: str, value: list):
    if not isinstance(value, list): raise TypeError("Value must be a list")
    dct[key] = value

def put_tuple(dct: dict, key: str, value: tuple):
    if not isinstance(value, tuple): raise TypeError("Value must be a tupple")
    dct[key] = value

def put_dict(dct: dict, key: str, value: dict):
    if not isinstance(value, dict): raise TypeError("Value must be a dictionary")
    dct[key] = value
