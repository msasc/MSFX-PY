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
from datetime import datetime, time, date
from decimal import Decimal
from importlib import import_module
from typing import Optional
from msfx.lib_back2 import error_msg

""" JSON extensions for data notation. """

valid_types = [bool, int, float, Decimal, complex, str, date, time, datetime, bytes, bytearray, list, dict]

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

registered_classes = {}

def register_class(key: str, clazz):
    registered_classes[key] = f"{clazz.__module__}.{clazz.__qualname__}"

def __instantiate_class(key, *args, **kwargs):
    if key in registered_classes:
        class_name = registered_classes[key]
        module_path, class_name = class_name.rsplit('.', 1)
        module = import_module(module_path)
        clazz = getattr(module, class_name)
        instance = clazz(*args, **kwargs)
        return instance
    return None

def __serializer(obj):

    # Extended JSON types: date, time, datetie, decimal, complex and binary.
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

    # Registered full class names.
    class_name = f"{type(obj).__module__}.{type(obj).__qualname__}"
    for key, registered_class_name in registered_classes.items():
        if class_name == registered_class_name:
            return {key: obj.to_dict()}

    # Not supported.
    raise TypeError(f"Type {type(obj)} not serializable")

def __deserializer(dct):

    # Extended JSON types: date, time, datetie, decimal, complex and binary.
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

    # Registered full class names.
    for key in registered_classes:
        if key in dct:
            data = dct[key]
            instance = __instantiate_class(key, data)
            if instance is not None:
                return instance

    # Return content as default.
    return dct

def dumps(dct: dict, **kwargs) -> str: return json.dumps(dct, default=__serializer, **kwargs)
def loads(obj) -> dict: return json.loads(obj, object_hook=__deserializer)

def get_bool(data: dict, key: str, default=False) -> bool:
    value = data.get(key, default)
    if isinstance(value, bool): return value
    raise TypeError(f"pair key {key} / value {value} is not a number")

def get_integer(data: dict, key: str, default=0) -> int:
    value = data.get(key, default)
    if isinstance(value, (int, float, Decimal)): return int(value)
    if isinstance(value, complex): return int(value.real)
    raise TypeError(f"pair key {key} / value {value} is not a number")

def get_float(data: dict, key: str, default=0.0) -> float:
    value = data.get(key, default)
    if isinstance(value, (int, float, Decimal)): return float(value)
    if isinstance(value, complex): return float(value.real)
    raise TypeError(f"pair key {key} / value {value} is not a number")

def get_decimal(data: dict, key: str, default=Decimal(0)) -> Decimal:
    value = data.get(key, default)
    if isinstance(value, (int, float, Decimal)): return Decimal(value)
    if isinstance(value, complex): return Decimal(value.real)
    raise TypeError(f"pair key {key} / value {value} is not a number")

def get_complex(data: dict, key: str, default=complex(0, 0)) -> complex:
    value = data.get(key, default)
    if isinstance(value, (int, float, Decimal, complex)): return complex(value)
    raise TypeError(f"pair key {key} / value {value} is not a number")

def get_string(data: dict, key: str, default="") -> str:
    value = data.get(key, default)
    if isinstance(value, str): return value
    raise TypeError(f"pair key {key} / value {value} is not a string")

def get_date(data: dict, key: str, default=None) -> Optional[date]:
    value = data.get(key, default)
    if isinstance(value, date): return value
    if isinstance(value, datetime): return value.date()
    if value is None: return None
    raise TypeError(f"pair key {key} / value {value} is not a date or datetime")

def get_time(data: dict, key: str, default=None) -> Optional[time]:
    value = data.get(key, default)
    if isinstance(value, time): return value
    if isinstance(value, datetime): return value.time()
    if value is None: return None
    raise TypeError(f"pair key {key} / value {value} is not a time or datetime")

def get_datetime(data: dict, key: str, default=None) -> Optional[datetime]:
    value = data.get(key, default)
    if isinstance(value, datetime): return value
    if value is None: return None
    raise TypeError(f"pair key {key} / value {value} is not a datetime")

def get_binary(data: dict, key: str, default=None) -> bytes or bytearray:
    value = data.get(key, default)
    if isinstance(value, (bytes, bytearray)): return value
    if value is None: return None
    raise TypeError(f"pair key {key} / value {value} is not a binary")

def get_list(data: dict, key: str, default=None) -> list:
    value = data.get(key, default)
    if isinstance(value, list): return value
    if value is None: return []
    raise TypeError(f"pair key {key} / value {value} is not a list")

def get_dict(data: dict, key: str, default=None) -> dict:
    value = data.get(key, default)
    if isinstance(value, dict): return value
    if value is None: return {}
    raise TypeError(f"pair key {key} / value {value} is not a dictionary")

def put_bool(data: dict, key: str, value: bool):
    if not isinstance(value, bool): raise TypeError("Value must be a boolean")
    data[key] = value

def put_integer(data: dict, key: str, value: int):
    if not isinstance(value, int): raise TypeError("Value must be an integer")
    data[key] = value

def put_float(data: dict, key: str, value: float):
    if not isinstance(value, float): raise TypeError("Value must be a float")
    data[key] = value

def put_complex(data: dict, key: str, value: complex):
    if not isinstance(value, complex): raise TypeError("Value must be a complex")
    data[key] = value

def put_decimal(data: dict, key: str, value: Decimal):
    if not isinstance(value, Decimal): raise TypeError("Value must be a decimal")
    data[key] = value

def put_string(data: dict, key: str, value: str):
    if not isinstance(value, str): raise TypeError("Value must be a string")
    data[key] = value

def put_date(data: dict, key: str, value: date):
    if not isinstance(value, date): raise TypeError("Value must be a date")
    data[key] = value

def put_time(data: dict, key: str, value: time):
    if not isinstance(value, time): raise TypeError("Value must be a time")
    data[key] = value

def put_datetime(data: dict, key: str, value: datetime):
    if not isinstance(value, datetime): raise TypeError("Value must be a datetime")
    data[key] = value

def put_binary(data: dict, key: str, value: (bytes, bytearray)):
    if not isinstance(value, (bytes, bytearray)): raise TypeError("Value must be a binary")
    data[key] = value

def put_list(data: dict, key: str, value: list):
    if not isinstance(value, list): raise TypeError("Value must be a list")
    # validate_list(value)
    data[key] = value

def put_dict(data: dict, key: str, value: dict):
    if not isinstance(value, dict): raise TypeError("Value must be a dictionary")
    # validate_dict(value)
    data[key] = value
