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

from datetime import date, time, datetime
from decimal import Decimal

from msfx.lib_back2.db_back2.types import Types

class Value:
    """ Encapsulates an immutable value of one of the supported types. """
    def __init__(self, value):
        # Argument value can not be None: either it is a non None value,
        # or a type which value can be None.
        if value is None: raise TypeError(f"Value can not be {None}.")

        # If value is an instance of Types is must be one of the types
        # that are nullable (DATE, TIME, DATETIME and BINARY.
        if isinstance(value, Types):
            if value not in Types.get_types_null():
                raise TypeError(f"Only types {Types.get_types_null()} accept a None value")

        self.__value = None
        self.__type = None

        # The type is passed as argument value is None, and we are done.
        if isinstance(value, Types):
            self.__type = value
            return

        # Assing the proper type or raise an exception if not supported.
        self.__type = Types.get_type(value)

        # Assign the value.
        self.__value = value

    def type(self) -> Types:
        return self.__type
    def value(self) -> object:
        return self.__value

    def is_none(self) -> bool:
        return self.__value is None
    def is_boolean(self) -> bool:
        return self.__type == Types.BOOLEAN
    def is_decimal(self) -> bool:
        return self.__type == Types.DECIMAL
    def is_integer(self) -> bool:
        return self.__type == Types.INTEGER
    def is_float(self) -> bool:
        return self.__type == Types.FLOAT
    def is_complex(self) -> bool:
        return self.__type == Types.COMPLEX
    def is_date(self) -> bool:
        return self.__type == Types.DATE
    def is_time(self) -> bool:
        return self.__type == Types.TIME
    def is_datetime(self) -> bool:
        return self.__type == Types.DATETIME
    def is_binary(self) -> bool:
        return self.__type == Types.BINARY
    def is_string(self) -> bool:
        return self.__type == Types.STRING
    def is_list(self) -> bool:
        return self.__type == Types.LIST
    def is_dictionary(self) -> bool:
        return self.__type == Types.DICTIONARY

    def is_numeric(self) -> bool:
        return self.__type in Types.get_types_numeric()

    def get_boolean(self) -> bool:
        if not self.is_boolean():
            raise TypeError("Type is not BOOLEAN")
        if self.is_none():
            return False
        return bool(self.__value)
    def get_decimal(self) -> Decimal:
        if not self.is_numeric():
            raise TypeError("Type is not NUMERIC")
        if self.is_none():
            return Decimal(0)
        if self.is_complex():
            return Decimal(self.__value.real)
        return Decimal(self.__value)
    def get_integer(self) -> int:
        if not self.is_numeric():
            raise TypeError("Type is not NUMERIC")
        if self.is_none():
            return 0
        if self.is_complex():
            return int(self.__value.real)
        return int(self.__value)
    def get_float(self) -> float:
        if not self.is_numeric():
            raise TypeError("Type is not NUMERIC")
        if self.is_none():
            return 0.0
        if self.is_complex():
            return float(self.__value.real)
        return float(self.__value)
    def get_complex(self) -> complex:
        if not self.is_numeric():
            raise TypeError("Type is not NUMERIC")
        if self.is_none():
            return complex(0)
        return complex(self.__value)
    def get_date(self) -> date or None:
        if not self.is_date():
            raise TypeError("Type is not DATE.")
        if self.is_none():
            return None
        return self.__value
    def get_time(self) -> time or None:
        if not self.is_time():
            raise TypeError("Type is not TIME.")
        if self.is_none():
            return None
        return self.__value
    def get_datetime(self) -> datetime or None:
        if not self.is_datetime():
            raise TypeError("Type is not DATETIME.")
        if self.is_none():
            return None
        return self.__value
    def get_binary(self) -> bytes:
        if not self.is_binary():
            raise TypeError("Type is not BINARY.")
        if self.is_none():
            return bytes([])
        return self.__value
    def get_string(self) -> str:
        if not self.is_string():
            raise TypeError("Type is not STRING.")
        if self.is_none():
            return ""
        return self.__value
    def get_list(self) -> list:
        if not self.is_list():
            raise TypeError("Type is not LIST.")
        if self.is_none():
            return []
        return self.__value
    def get_dictionary(self) -> dict:
        if not self.is_dictionary():
            raise TypeError("Type is not DICTIONARY.")
        if self.is_none():
            return {}
        return self.__value

    def compare_to(self, other) -> int:
        if self.__eq__(other):
            return 0
        if self.__lt__(other):
            return -1
        return 1

    def is_comparable(self, other) -> bool:
        if isinstance(other, Value):
            if self.is_numeric() and other.is_numeric():
                return True
            if self.__type == other.__type:
                return True
            return False
        if self.is_boolean():
            return isinstance(other, bool)
        if self.is_numeric():
            return isinstance(other, (int, float, complex, Decimal))
        if self.is_date():
            return isinstance(other, date)
        if self.is_time():
            return isinstance(other, time)
        if self.is_datetime():
            return isinstance(other, datetime)
        if self.is_binary():
            return isinstance(other, bytes)
        if self.is_string():
            return isinstance(other, str)
        if self.is_list():
            return isinstance(other, dict)
        if self.is_dictionary():
            return isinstance(other, dict)
        return False

    def __lt__(self, other) -> bool:
        if isinstance(other, Value):
            return self.__value < other.__value
        if self.is_comparable(other):
            return self.__value < other
        raise TypeError(f"Not comparable value {other}")
    def __le__(self, other) -> bool:
        if isinstance(other, Value):
            return self.__value <= other.__value
        if self.is_comparable(other):
            return self.__value <= other
        raise TypeError(f"Not comparable value {other}")
    def __eq__(self, other) -> bool:
        if isinstance(other, Value):
            return self.__value == other.__value
        if self.is_comparable(other):
            return self.__value == other
        raise TypeError(f"Not comparable value {other}")
    def __ne__(self, other) -> bool:
        if isinstance(other, Value):
            return self.__value != other.__value
        if self.is_comparable(other):
            return self.__value != other
        raise TypeError(f"Not comparable value {other}")
    def __gt__(self, other) -> bool:
        if isinstance(other, Value):
            return self.__value > other.__value
        if self.is_comparable(other):
            return self.__value > other
        raise TypeError(f"Not comparable value {other}")
    def __ge__(self, other) -> bool:
        if isinstance(other, Value):
            return self.__value >= other.__value
        if self.is_comparable(other):
            return self.__value >= other
        raise TypeError(f"Not comparable value {other}")
    def __str__(self) -> str:
        return str(self.__value)
    def __repr__(self):
        if self.is_string():
            return "'" + str(self.__value) + "'"
        return self.__str__()
