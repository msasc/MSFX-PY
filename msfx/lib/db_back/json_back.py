#  Copyright (c) 2023-2024 Miquel Sas.
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
import base64
import decimal

import json
from datetime import date, time, datetime
from decimal import Decimal

class JSON:
    """
    A JSON implementation that supports the standard number, string, boolean and null types,
    as well as the extended date, time, datetime, binary and decimal. The decimal type
    preserves the original scale.
    """
    def __init__(self, json_data=None):
        self.__data: dict = {}
        if json_data is not None:
            self.loads(json_data)

    def __serializer(self, obj):
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

    def __deserializer(self, dct):
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

    def loads(self, json_data):
        self.__data |= json.loads(json_data, object_hook=self.__deserializer)

    def dumps(self, **kwargs) -> str:
        return json.dumps(self.__data, default=self.__serializer, **kwargs)

    def merge(self, data: dict):
        if type(data) is not dict:
            raise "Data to merge must be of dict type"
        self.__data |= data

    def data(self) -> dict:
        return self.__data

    def contains(self, key: str) -> bool:
        return key in self.__data

    def get_bool(self, key: str) -> bool:
        value = self.__data.get(key)
        if isinstance(value, bool): return value
        raise TypeError(f"pair key {key} / value {value} is not a boolean")

    def get_integer(self, key: str) -> int:
        value = self.__data.get(key)
        if isinstance(value, (int, float, Decimal)): return int(value)
        if isinstance(value, complex): return int(value.real)
        raise TypeError(f"pair key {key} / value {value} is not a number")

    def get_float(self, key: str) -> float:
        value = self.__data.get(key)
        if isinstance(value, (int, float, Decimal)): return float(value)
        if isinstance(value, complex): return float(value.real)
        raise TypeError(f"pair key {key} / value {value} is not a number")

    def get_decimal(self, key: str) -> decimal:
        value = self.__data.get(key)
        if isinstance(value, (int, float, Decimal)): return Decimal(value)
        if isinstance(value, complex): return Decimal(value.real)
        raise TypeError(f"pair key {key} / value {value} is not a number")

    def get_string(self, key: str) -> str:
        value = self.__data.get(key)
        if isinstance(value, str): return value
        raise TypeError(f"pair key {key} / value {value} is not a string")

    def get_date(self, key: str) -> date:
        value = self.__data.get(key)
        if isinstance(value, date): return value
        if isinstance(value, datetime): return value.date()
        raise TypeError(f"pair key {key} / value {value} is not a date or datetime")

    def get_time(self, key: str) -> time:
        value = self.__data.get(key)
        if isinstance(value, time): return value
        if isinstance(value, datetime): return value.time()
        raise TypeError(f"pair key {key} / value {value} is not a time or datetime")

    def get_binary(self, key: str) -> bytes or bytearray:
        value = self.__data.get(key)
        if isinstance(value, (bytes, bytearray)): return value
        raise TypeError(f"pair key {key} / value {value} is not a binary")

    def get_tuple(self, key: str) -> tuple:
        value = self.__data.get(key)
        if isinstance(value, tuple): return value
        raise TypeError(f"pair key {key} / value {value} is not a tuple")

    def get_list(self, key: str) -> list:
        value = self.__data.get(key)
        if isinstance(value, list): return value
        raise TypeError(f"pair key {key} / value {value} is not a list")

    def get_dict(self, key: str) -> dict:
        value = self.__data.get(key)
        if isinstance(value, dict): return value
        raise TypeError(f"pair key {key} / value {value} is not a dictionary")

    def get_json(self, key: str) -> object:
        value = self.__data.get(key)
        if isinstance(value, dict):
            js = JSON()
            js.__data = value
            return js
        raise TypeError(f"pair key {key} / value {value} is not a dictionary")

    def is_bool(self, key: str) -> bool:
        value = self.__data.get(key)
        return isinstance(value, bool)

    def put_bool(self, key: str, value: bool):
        if not isinstance(value, bool):
            raise TypeError("Value must be a boolean")
        self.__data[key] = value

    def put_integer(self, key: str, value: int):
        if not isinstance(value, int):
            raise TypeError("Value must be an integer")
        self.__data[key] = value

    def put_float(self, key: str, value: float):
        if not isinstance(value, float):
            raise TypeError("Value must be a float")
        self.__data[key] = value

    def put_complex(self, key: str, value: complex):
        if not isinstance(value, complex):
            raise TypeError("Value must be a complex")
        self.__data[key] = value

    def put_decimal(self, key: str, value: Decimal):
        if not isinstance(value, Decimal):
            raise TypeError("Value must be a decimal")
        self.__data[key] = value

    def put_string(self, key: str, value: str):
        self.__data[key] = value

    def put_date(self, key: str, value: date):
        if not isinstance(value, date):
            raise TypeError("Value must be a date")
        self.__data[key] = value

    def put_time(self, key: str, value: time):
        if not isinstance(value, time):
            raise TypeError("Value must be a time")
        self.__data[key] = value

    def put_datetime(self, key: str, value: datetime):
        if not isinstance(value, datetime):
            raise TypeError("Value must be a datetime")
        self.__data[key] = value

    def put_binary(self, key: str, value: (bytes, bytearray)):
        if not isinstance(value, (bytes, bytearray)):
            raise TypeError("Value must be a binary")
        self.__data[key] = value

    def put_list(self, key: str, value: list):
        if not isinstance(value, list):
            raise TypeError("Value must be a list")
        self.__data[key] = value

    def put_tuple(self, key: str, value: tuple):
        if not isinstance(value, tuple):
            raise TypeError("Value must be a tupple")
        self.__data[key] = value

    def put_dict(self, key: str, value: dict):
        if not isinstance(value, dict):
            raise TypeError("Value must be a dictionary")
        self.__data[key] = value

    def put_json(self, key: str, value: (dict, object)):
        if not isinstance(value, JSON):
            raise TypeError("Value must be a JSON")
        self.__data[key] = value.data()

    def is_bool(self, key: str) -> bool:
        pass

    def __str__(self) -> str:
        return str(self.__data)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, JSON):
            return self.__data == other.__data
        if isinstance(other, dict):
            return self.__data == other
        return super().__eq__(other)