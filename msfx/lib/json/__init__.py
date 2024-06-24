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

import json
from datetime import date, datetime, time
from decimal import Decimal
from importlib import import_module
from typing import Optional

from msfx.lib.util.globals import error_msg, instantiate

registered_classes = {}
def register_class(key: str, clazz):
    registered_classes[key] = f"{clazz.__module__}.{clazz.__qualname__}"

def instantiate_class(key, *args, **kwargs):
    if key in registered_classes:
        full_class_name = registered_classes[key]
        instance = instantiate(full_class_name,*args, **kwargs)
        return instance
    return None


def __serializer(obj):
    if isinstance(obj, date) and not isinstance(obj, datetime):
        return {"date": obj.isoformat()}
    if isinstance(obj, time):
        return {"time": obj.isoformat()}
    if isinstance(obj, datetime):
        return {"datetime": obj.isoformat()}
    if isinstance(obj, Decimal):
        return {"decimal": str(obj)}
    if isinstance(obj, complex):
        return {"complex": str(obj)}
    if isinstance(obj, (bytes, bytearray)):
        return {"binary": obj.hex()}
    if type(obj).__name__ == "Column":
        return {"column": obj.to_dict()}
    raise TypeError(f"Type {type(obj)} not serializable")

def __deserializer(dct):
    if "date" in dct:
        return date.fromisoformat(dct["date"])
    if "time" in dct:
        return time.fromisoformat(dct["time"])
    if "datetime" in dct:
        return datetime.fromisoformat(dct["datetime"])
    if "decimal" in dct:
        return Decimal(dct["decimal"])
    if "complex" in dct:
        return complex(dct["complex"])
    if "binary" in dct:
        return bytes.fromhex(dct["binary"])
    if "column" in dct:
        data = dct["column"]
        instance = instantiate_class("column", data)
        if instance is not None:
            return instance
    return dct

def dumps(dct: dict, **kwargs) -> str: return json.dumps(dct, default=__serializer, **kwargs)
def loads(obj) -> dict: return json.loads(obj, object_hook=__deserializer)

valid_types = [bool, int, float, Decimal, complex, str, date, time, datetime, bytes, bytearray, list, dict]

def validate_value(value: object):
    if isinstance(value, bool): return
    if isinstance(value, (int, float, complex, Decimal)): return
    if isinstance(value, str): return
    if isinstance(value, (date, time, datetime)): return
    if isinstance(value, (bytes, bytearray)): return
    if isinstance(value, list): validate_list(value)
    if isinstance(value, dict): validate_dict(value)
    raise ValueError(f"Invalid value {value} of type {type(value)}")
def validate_list(lst: (list, tuple)):
    if not isinstance(lst, (list, tuple)): raise TypeError("Value must be a list or tuple")
    for value in lst: validate_value(value)
def validate_dict(dct: dict):
    if not isinstance(dct, dict): raise TypeError("Value must be a dictionary")
    for key, value in dct.items(): validate_value(value)

class Schema:

    def __init__(self):
        self.__fields = {}

    def add(self, key: str, value_type: type, default_value: object):
        if value_type not in valid_types:
            error = error_msg("type error", "value_type", value_type, valid_types)
            raise TypeError(error)
        if default_value is not None and not isinstance(default_value, value_type):
            error = error_msg("value error", "default_value", default_value, value_type)
            raise ValueError(error)
        self.__fields[key] = {"type": value_type, "default": default_value}

    def fields(self) -> dict: return dict(self.__fields)

    def __str__(self) -> str:
        return str(dumps(self.__fields))
    def __repr__(self):
        return self.__str__()
    def __iter__(self):
        return self.__fields.__iter__()
    def __len__(self) -> int:
        return len(self.__fields)

def create_from_schema(schema: Schema) -> dict:
    data = {}
    for key, value in schema.fields().items():
        default_value = value["default"]
        data[key] = default_value
    return data

def create_from_kwargs(schema: Schema, **kwargs) -> dict:
    data = {}
    for key, value in schema.fields().items():
        value_type = value["type"]
        if key in kwargs:
            arg_value = kwargs[key]
            if arg_value is not None and not isinstance(arg_value, value_type):
                error = error_msg("type error", arg_value, type(arg_value), (value_type,))
                raise TypeError(error)
            data[key] = arg_value
    return data

class JSON:
    """ JSON extension. """
    def __init__(self, obj=None):
        self.__data = {}
        if obj is not None and isinstance(obj, dict):
            self.__data |= obj
        if obj is not None and isinstance(obj, JSON):
            self.__data |= obj.__data
        if obj is not None and isinstance(obj, str):
            self.__data |= loads(obj)
        if obj is not None and isinstance(obj, Schema):
            self.__data = create_from_schema(obj)

    def merge(self, obj=None):
        if obj is not None:
            if not isinstance(obj, (JSON, dict)):
                error = error_msg("type error", "obj", type(obj), (JSON, dict))
                raise TypeError(error)
            if isinstance(obj, JSON):
                self.__data |= obj.__data
            if isinstance(obj, dict):
                self.__data |= obj

    def get_bool(self, key: str, default=False) -> bool:
        value = self.__data.get(key, default)
        if isinstance(value, bool): return value
        raise TypeError(f"pair key {key} / value {value} is not a number")

    def get_integer(self, key: str, default=0) -> int:
        value = self.__data.get(key, default)
        if isinstance(value, (int, float, Decimal)): return int(value)
        if isinstance(value, complex): return int(value.real)
        raise TypeError(f"pair key {key} / value {value} is not a number")

    def get_float(self, key: str, default=0.0) -> float:
        value = self.__data.get(key, default)
        if isinstance(value, (int, float, Decimal)): return float(value)
        if isinstance(value, complex): return float(value.real)
        raise TypeError(f"pair key {key} / value {value} is not a number")

    def get_decimal(self, key: str, default=Decimal(0)) -> Decimal:
        value = self.__data.get(key, default)
        if isinstance(value, (int, float, Decimal)): return Decimal(value)
        if isinstance(value, complex): return Decimal(value.real)
        raise TypeError(f"pair key {key} / value {value} is not a number")

    def get_complex(self, key: str, default=complex(0, 0)) -> complex:
        value = self.__data.get(key, default)
        if isinstance(value, (int, float, Decimal, complex)): return complex(value)
        raise TypeError(f"pair key {key} / value {value} is not a number")

    def get_string(self, key: str, default="") -> str:
        value = self.__data.get(key, default)
        if isinstance(value, str): return value
        raise TypeError(f"pair key {key} / value {value} is not a string")

    def get_date(self, key: str, default=None) -> Optional[date]:
        value = self.__data.get(key, default)
        if isinstance(value, date): return value
        if isinstance(value, datetime): return value.date()
        if value is None: return None
        raise TypeError(f"pair key {key} / value {value} is not a date or datetime")

    def get_time(self, key: str, default=None) -> Optional[time]:
        value = self.__data.get(key, default)
        if isinstance(value, time): return value
        if isinstance(value, datetime): return value.time()
        if value is None: return None
        raise TypeError(f"pair key {key} / value {value} is not a time or datetime")

    def get_datetime(self, key: str, default=None) -> Optional[datetime]:
        value = self.__data.get(key, default)
        if isinstance(value, datetime): return value
        if value is None: return None
        raise TypeError(f"pair key {key} / value {value} is not a datetime")

    def get_binary(self, key: str, default=None) -> bytes or bytearray:
        value = self.__data.get(key, default)
        if isinstance(value, (bytes, bytearray)): return value
        if value is None: return None
        raise TypeError(f"pair key {key} / value {value} is not a binary")

    def get_list(self, key: str, default=None) -> list:
        value = self.__data.get(key, default)
        if isinstance(value, list): return value
        if value is None: return []
        raise TypeError(f"pair key {key} / value {value} is not a list")

    def get_dict(self, key: str, default=None) -> dict:
        value = self.__data.get(key, default)
        if isinstance(value, dict): return value
        if value is None: return {}
        raise TypeError(f"pair key {key} / value {value} is not a dictionary")

    def put_bool(self, key: str, value: bool):
        if not isinstance(value, bool): raise TypeError("Value must be a boolean")
        self.__data[key] = value

    def put_integer(self, key: str, value: int):
        if not isinstance(value, int): raise TypeError("Value must be an integer")
        self.__data[key] = value

    def put_float(self, key: str, value: float):
        if not isinstance(value, float): raise TypeError("Value must be a float")
        self.__data[key] = value

    def put_complex(self, key: str, value: complex):
        if not isinstance(value, complex): raise TypeError("Value must be a complex")
        self.__data[key] = value

    def put_decimal(self, key: str, value: Decimal):
        if not isinstance(value, Decimal): raise TypeError("Value must be a decimal")
        self.__data[key] = value

    def put_string(self, key: str, value: str):
        if not isinstance(value, str): raise TypeError("Value must be a string")
        self.__data[key] = value

    def put_date(self, key: str, value: date):
        if not isinstance(value, date): raise TypeError("Value must be a date")
        self.__data[key] = value

    def put_time(self, key: str, value: time):
        if not isinstance(value, time): raise TypeError("Value must be a time")
        self.__data[key] = value

    def put_datetime(self, key: str, value: datetime):
        if not isinstance(value, datetime): raise TypeError("Value must be a datetime")
        self.__data[key] = value

    def put_binary(self, key: str, value: (bytes, bytearray)):
        if not isinstance(value, (bytes, bytearray)): raise TypeError("Value must be a binary")
        self.__data[key] = value

    def put_list(self, key: str, value: list):
        if not isinstance(value, list): raise TypeError("Value must be a list")
        validate_list(value)
        self.__data[key] = value

    def put_dict(self, key: str, value: dict):
        if not isinstance(value, dict): raise TypeError("Value must be a dictionary")
        validate_dict(value)
        self.__data[key] = value

    def to_dict(self):
        return dict(self.__data)

    def to_string(self, **kwargs):
        return dumps(self.__data, **kwargs)

    def __str__(self) -> str:
        return dumps(self.__data)
    def __repr__(self):
        return self.__str__()
    def __iter__(self):
        return self.__data.__iter__()
    def __len__(self) -> int:
        return len(self.__data)
