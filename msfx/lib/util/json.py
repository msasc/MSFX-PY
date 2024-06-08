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
    def __init__(self, json_data=None):
        """ Creates a JSON object dumping json string data. """
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
        # Add more cases if needed
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
        # Add more cases if needed
        return dct

    def loads(self, json_data):
        """ Loads the argument json_data string and merges it with this JSON internal dictionary data. """
        self.__data |= json.loads(json_data, object_hook=self.__deserializer)

    def dumps(self, **kwargs) -> str:
        """ Dumps the internal dictionary data and returns a json string representation. """
        return json.dumps(self.__data, default=self.__serializer, **kwargs)

    def merge(self, data: dict):
        """ Merges the argument dictionary data with this JSON internal dictionary data. """
        if type(data) is not dict:
            raise "Data to merge must be of dict type"
        self.__data |= data

    def data(self) -> dict:
        """ Gives access to the internal Python data dictionary. """
        return self.__data

    def put_bool(self, key: str, value: bool):
        if not isinstance(value, bool):
            raise Exception("Value must be a boolean")
        self.__data[key] = value

    def put_int(self, key: str, value: int):
        if not isinstance(value, int):
            raise Exception("Value must be an integer")
        self.__data[key] = value

    def put_float(self, key: str, value: float):
        if not isinstance(value, float):
            raise Exception("Value must be a float")
        self.__data[key] = value

    def put_decimal(self, key: str, value: Decimal):
        if not isinstance(value, Decimal):
            raise Exception("Value must be a decimal")
        self.__data[key] = value

    def put_string(self, key: str, value: str):
        self.__data[key] = value

    def put_date(self, key: str, value: date):
        if not isinstance(value, date):
            raise Exception("Value must be a date")
        self.__data[key] = value

    def put_time(self, key: str, value: time):
        if not isinstance(value, time):
            raise Exception("Value must be a time")
        self.__data[key] = value

    def put_datetime(self, key: str, value: datetime):
        if not isinstance(value, datetime):
            raise Exception("Value must be a datetime")
        self.__data[key] = value

    def put_binary(self, key: str, value: (bytes, bytearray)):
        if not isinstance(value, (bytes, bytearray)):
            raise Exception("Value must be a binary")
        self.__data[key] = value

    def get(self, key: str):
        if key in self.__data:
            return self.__data[key]
        return None

    def get_bool(self, key: str) -> bool:
        if key in self.__data:
            value = self.__data[key]
            if isinstance(value, bool):
                return value
            raise Exception(f"pair key {key} / value {value} is not a boolean")
        raise Exception(f"Invalid key: {key}")

    def get_int(self, key: str) -> int:
        if key in self.__data:
            value = self.__data[key]
            if isinstance(value, (int, float, Decimal)):
                return int(value)
            raise Exception(f"pair key {key} / value {value} is not a number")
        raise Exception(f"Invalid key: {key}")

    def get_float(self, key: str) -> float:
        if key in self.__data:
            value = self.__data[key]
            if isinstance(value, (int, float, Decimal)):
                return float(value)
            raise Exception(f"pair key {key} / value {value} is not a number")
        raise Exception(f"Invalid key: {key}")

    def get_decimal(self, key: str) -> decimal:
        if key in self.__data:
            value = self.__data[key]
            if isinstance(value, (int, float, Decimal)):
                return Decimal(value)
            raise Exception(f"pair key {key} / value {value} is not a number")
        raise Exception(f"Invalid key: {key}")

    def get_string(self, key: str) -> str:
        if key in self.__data:
            value = self.__data[key]
            if isinstance(value, str):
                return value
            raise Exception(f"pair key {key} / value {value} is not a string")
        raise Exception(f"Invalid key: {key}")

    def get_date(self, key: str) -> date:
        if key in self.__data:
            value = self.__data[key]
            if isinstance(value, date):
                return value
            if isinstance(value, datetime):
                return value.date()
            raise Exception(f"pair key {key} / value {value} is not a date or datetime")
        raise Exception(f"Invalid key: {key}")

    def get_time(self, key: str) -> time:
        if key in self.__data:
            value = self.__data[key]
            if isinstance(value, time):
                return value
            if isinstance(value, datetime):
                return value.time()
            raise Exception(f"pair key {key} / value {value} is not a time or datetime")
        raise Exception(f"Invalid key: {key}")

    def get_binary(self, key: str) -> bytes or bytearray:
        if key in self.__data:
            value = self.__data[key]
            if isinstance(value, (bytes, bytearray)):
                return value
            raise Exception(f"pair key {key} / value {value} is not a binary")
        raise Exception(f"Invalid key: {key}")

    def __str__(self) -> str:
        return str(self.__data)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, JSON):
            return self.__data == other.__data
        if isinstance(other, dict):
            return self.__data == other
        return super().__eq__(other)
