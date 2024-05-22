#  Copyright (c) 2023 Miquel Sas.
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

from decimal import Decimal
from datetime import date, time, datetime

from msfx.lib.db.json import JSON
from msfx.lib.db.types import Types, TYPES_NULL

class Value:
    """ Encapsulates an immutable value of one of the supported types. """
    def __init__(self, value):
        """
        Constructs a Value with one of the supported types.
        :param value: The data value or the Types type and the internal value will be None.
        """
        # Argument value can not be None: either it is a non None value, or a type which value can be None.
        if value is None:
            raise Exception("Value can not be none.")

        # Value is an instance of Types, thus the value itself is None and the type must be one of
        # DATE, TIME, DATETIME or BINARY.
        if isinstance(value, Types):
            if value not in TYPES_NULL:
                raise Exception("Only types DATE, TIME, TIMESTAMP and BINARY accept a None value")

        self.__value = None
        self.__type = None

        # The type is passed as argument value is None, and we are done.
        if isinstance(value, Types):
            self.__type = value
            return

        # Assing the proper type or raise an exception if not supported.
        if isinstance(value, bool):
            self.__type = Types.BOOLEAN
        elif isinstance(value, Decimal):
            self.__type = Types.DECIMAL
        elif isinstance(value, int):
            self.__type = Types.INTEGER
        elif isinstance(value, float):
            self.__type = Types.FLOAT
        elif isinstance(value, complex):
            self.__type = Types.COMPLEX
        elif isinstance(value, date):
            self.__type = Types.DATE
        elif isinstance(value, time):
            self.__type = Types.TIME
        elif isinstance(value, datetime):
            self.__type = Types.DATETIME
        elif isinstance(value, bytes):
            self.__type = Types.BINARY
        elif isinstance(value, str):
            self.__type = Types.STRING
        elif isinstance(value, JSON):
            self.__type = Types.JSON
        else: raise Exception(f"Invalid type for argument value: {type(value)}")

        # Assign the value.
        self.__value = value

    def type(self) -> Types:
        """
        Return the type.
        :return: The type of the value, even if the vlue is None.
        """
        return self.__type

    def value(self) -> object:
        """
        Return the value.
        :return: The internal value.
        """
        return self.__value

    def is_none(self) -> bool:
        """
        Check whether the value is None.
        :return: A bool.
        """
        return self.__value is None
    def is_boolean(self) -> bool:
        """
        Check whether the value is boolean.
        :return: A bool.
        """
        return self.__type == Types.BOOLEAN
    def is_decimal(self) -> bool:
        """
        Check whether the value is a decimal.
        :return: A bool.
        """
        return self.__type == Types.DECIMAL
    def is_integer(self) -> bool:
        """
        Check whether the value is an integer.
        :return: A bool.
        """
        return self.__type == Types.INTEGER
    def is_float(self) -> bool:
        """
        Check whether the value is a float.
        :return: A bool.
        """
        return self.__type == Types.FLOAT
    def is_complex(self) -> bool:
        """
        Check whether the value is a complex.
        :return: A bool.
        """
        return self.__type == Types.COMPLEX
    def is_date(self) -> bool:
        """
        Check whether the value is a date. A date value can be None.
        :return: A bool.
        """
        return self.__type == Types.DATE
    def is_time(self) -> bool:
        """
        Check whether the value is a time. A time value can be None.
        :return: A bool.
        """
        return self.__type == Types.TIME
    def is_datetime(self) -> bool:
        """
        Check whether the value is a date-time. A date-time value can be None.
        :return: A bool.
        """
        return self.__type == Types.DATETIME
    def is_binary(self) -> bool:
        """
        Check whether the value is a binary value. A binary value can be None.
        :return: A bool.
        """
        return self.__type == Types.BINARY
    def is_string(self) -> bool:
        """
        Check whether the value is a string.
        :return: A bool.
        """
        return self.__type == Types.STRING
    def is_JSON(self) -> bool:
        """
        Check whether this value is a JSON object.
        :return: A boolean.
        """
        return self.__type == Types.JSON

    def is_numeric(self) -> bool:
        """
        Check whether the value is a numeric value.
        :return: A bool.
        """
        numeric: bool = (
            self.__type == Types.DECIMAL or
            self.__type == Types.INTEGER or
            self.__type == Types.FLOAT or
            self.__type == Types.COMPLEX
        )
        return numeric

    def get_boolean(self) -> bool:
        """
        Returns the value as a boolean or raises an exception if it is not a boolean.
        :return: The boolean value.
        """
        if not self.is_boolean(): raise Exception("Type is not BOOLEAN")
        if self.is_none(): return False
        return bool(self.__value)
    def get_decimal(self) -> Decimal:
        """
        Returns the value as a decimal or raises an exception if it is not a numeric.
        :return: The decimal value.
        """
        if not self.is_numeric(): raise Exception("Type is not NUMERIC")
        if self.is_none(): return Decimal(0)
        if self.is_complex(): return Decimal(self.__value.real)
        return Decimal(self.__value)
    def get_integer(self) -> int:
        """
        Returns the value as an integer or raises an exception if it is not a numeric.
        :return: The integer value.
        """
        if not self.is_numeric(): raise Exception("Type is not NUMERIC")
        if self.is_none(): return 0
        if self.is_complex(): return int(self.__value.real)
        return int(self.__value)
    def get_float(self) -> float:
        """
        Returns the value as a float or raises an exception if it is not a numeric.
        :return: The float value.
        """
        if not self.is_numeric(): raise Exception("Type is not NUMERIC")
        if self.is_none(): return 0.0
        if self.is_complex(): return float(self.__value.real)
        return float(self.__value)
    def get_complex(self) -> complex:
        """
        Returns the value as a complex or raises an exception if it is not a numeric.
        :return: The complex value.
        """
        if not self.is_numeric(): raise Exception("Type is not NUMERIC")
        if self.is_none(): return complex(0)
        return complex(self.__value)
    def get_date(self) -> date or None:
        """
        Returns the value as a date or raises an exception if it is not a date.
        :return: The date value.
        """
        if not self.is_date(): raise Exception("Type is not DATE.")
        if self.is_none(): return None
        return self.__value
    def get_time(self) -> time or None:
        """
        Returns the value as a time or raises an exception if it is not a time.
        :return: The time value.
        """
        if not self.is_time(): raise Exception("Type is not TIME.")
        if self.is_none(): return None
        return self.__value
    def get_datetime(self) -> datetime or None:
        """
        Returns the value as a datetime or raises an exception if it is not a datetime.
        :return: The datetime value.
        """
        if not self.is_datetime(): raise Exception("Type is not DATETIME.")
        if self.is_none(): return None
        return self.__value
    def get_binary(self) -> bytes:
        """
        Returns the value as a binary or raises an exception if it is not a binary.
        :return: The binary value.
        """
        if not self.is_binary(): raise Exception("Type is not BINARY.")
        if self.is_none(): return bytes([])
        return self.__value
    def get_string(self) -> str:
        """
        Returns the value as a string or raises an exception if it is not a string.
        :return: The string value.
        """
        if not self.is_string(): raise Exception("Type is not STRING.")
        if self.is_none(): return ""
        return self.__value
    def get_JSON(self) -> JSON:
        """
        Returns the value as a JSON or raises an exception if it is not a JSON.
        :return: The JSON value.
        """
        if not self.is_JSON(): raise Exception("Type is not JSON.")
        if self.is_none(): return JSON()
        js: JSON = self.__value
        return JSON(js.dumps())

    def compare_to(self, other) -> int:
        """
        Compare for order.
        :param other: Another value.
        :return: The comparison integer.
        """
        if self.__eq__(other): return 0
        if self.__lt__(other): return -1
        return 1

    def is_comparable(self, other) -> bool:
        """
        Check whether this value is comparable to another object.
        :param other: Another object.
        :return: A boolean.
        """
        comparable: bool = False
        if self.is_boolean(): comparable = isinstance(other, bool)
        if self.is_numeric():
            comparable = (
                isinstance(other, Decimal) or
                isinstance(other, int) or
                isinstance(other, float) or
                isinstance(other, complex)
            )
        if self.is_date(): comparable = isinstance(other, date)
        if self.is_time(): comparable = isinstance(other, time)
        if self.is_datetime(): comparable = isinstance(other, datetime)
        if self.is_binary(): comparable = isinstance(other, bytes)
        if self.is_string(): comparable = isinstance(other, str)
        if self.is_JSON(): comparable = isinstance(other, JSON)
        return comparable

    def __lt__(self, other) -> bool:
        if isinstance(other, Value): return self.__value < other.__value
        if self.is_comparable(other): return self.__value < other
        raise TypeError(f"Not comparable value {other}")
    def __le__(self, other) -> bool:
        if isinstance(other, Value): return self.__value <= other.__value
        if self.is_comparable(other): return self.__value <= other
        raise TypeError(f"Not comparable value {other}")
    def __eq__(self, other) -> bool:
        if isinstance(other, Value): return self.__value == other.__value
        if self.is_comparable(other): return self.__value == other
        raise TypeError(f"Not comparable value {other}")
    def __ne__(self, other) -> bool:
        if isinstance(other, Value): return self.__value != other.__value
        if self.is_comparable(other): return self.__value != other
        raise TypeError(f"Not comparable value {other}")
    def __gt__(self, other) -> bool:
        if isinstance(other, Value): return self.__value > other.__value
        if self.is_comparable(other): return self.__value > other
        raise TypeError(f"Not comparable value {other}")
    def __ge__(self, other) -> bool:
        if isinstance(other, Value): return self.__value >= other.__value
        if self.is_comparable(other): return self.__value >= other
        raise TypeError(f"Not comparable value {other}")
    def __str__(self) -> str:
        if self.is_none(): return ""
        return str(self.__value)
