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

from datetime import date, time, datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Optional

class Types(Enum):
    """ Types accepted within this database SQL metadata. """
    BOOLEAN = "BOOLEAN"
    DECIMAL = "DECIMAL"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    COMPLEX = "COMPLEX"
    DATE = "DATE"
    TIME = "TIME"
    DATETIME = "DATETIME"
    BINARY = "BINARY"
    STRING = "STRING"
    LIST = "LIST"
    DICT = "DICT"

    @staticmethod
    def get_type(value: object):
        if isinstance(value, bool): return Types.BOOLEAN
        if isinstance(value, Decimal): return Types.DECIMAL
        if isinstance(value, int): return Types.INTEGER
        if isinstance(value, float): return Types.FLOAT
        if isinstance(value, date): return Types.DATE
        if isinstance(value, time): return Types.TIME
        if isinstance(value, datetime): return Types.DATETIME
        if isinstance(value, bytes): return Types.BINARY
        if isinstance(value, str): return Types.STRING
        if isinstance(value, (tuple, list)): return Types.LIST
        if isinstance(value, dict): return Types.DICT
        raise TypeError(f"Invalid type of value {value}")
    @staticmethod
    def get_types_none() -> tuple: return Types.DATE, Types.TIME, Types.DATETIME, Types.BINARY
    @staticmethod
    def get_types_numeric() -> tuple: return Types.INTEGER, Types.FLOAT, Types.DECIMAL, Types.COMPLEX
    @staticmethod
    def get_types_length() -> tuple: return Types.DECIMAL, Types.STRING, Types.BINARY

class Value:
    """ Encapsulates a mutable value of one of the supported types. """
    def __init__(self, value):
        # Argument value can not be None: either it is a non None value,
        # or a type which value can be None.
        if value is None: raise TypeError(f"Value can not be {None}.")

        # If value is an instance of Types is must be one of the types
        # that are nullable (DATE, TIME, DATETIME and BINARY.
        if isinstance(value, Types):
            if value not in Types.get_types_none():
                raise TypeError(f"Only types {Types.get_types_none()} accept a None value")

        self.__value = None
        self.__type: Optional[Types] = None
        self.__modified: bool = False

        # The type is passed as argument value is None, and we are done.
        if isinstance(value, Types):
            self.__type = value
            return

        # Assing the proper type or raise an exception if not supported.
        self.__type = Types.get_type(value)

        # Assign the value.
        self.__value = value

    def type(self) -> Types: return self.__type
    def value(self) -> object: return self.__value

    def is_modified(self) -> bool: return self.__modified

    def is_none(self) -> bool: return self.__value is None
    def is_boolean(self) -> bool: return self.__type == Types.BOOLEAN
    def is_decimal(self) -> bool: return self.__type == Types.DECIMAL
    def is_integer(self) -> bool: return self.__type == Types.INTEGER
    def is_float(self) -> bool: return self.__type == Types.FLOAT
    def is_complex(self) -> bool: return self.__type == Types.COMPLEX
    def is_numeric(self) -> bool: return self.__type in Types.get_types_numeric()
    def is_date(self) -> bool: return self.__type == Types.DATE
    def is_time(self) -> bool: return self.__type == Types.TIME
    def is_datetime(self) -> bool: return self.__type == Types.DATETIME
    def is_binary(self) -> bool: return self.__type == Types.BINARY
    def is_string(self) -> bool: return self.__type == Types.STRING
    def is_list(self) -> bool: return self.__type == Types.LIST
    def is_dict(self) -> bool: return self.__type == Types.DICT

    def get_boolean(self) -> bool:
        if not self.is_boolean(): raise TypeError("Type is not BOOLEAN")
        if self.is_none(): return False
        return bool(self.__value)
    def get_decimal(self) -> Decimal:
        if not self.is_numeric(): raise TypeError("Type is not NUMERIC")
        if self.is_none(): return Decimal(0)
        return Decimal(self.__value)
    def get_integer(self) -> int:
        if not self.is_numeric(): raise TypeError("Type is not NUMERIC")
        if self.is_none(): return 0
        return int(self.__value)
    def get_float(self) -> float:
        if not self.is_numeric(): raise TypeError("Type is not NUMERIC")
        if self.is_none(): return 0.0
        return float(self.__value)
    def get_complex(self) -> complex:
        if not self.is_numeric(): raise TypeError("Type is not NUMERIC")
        if self.is_none(): return complex(0, 0)
        return complex(self.__value)
    def get_date(self) -> Optional[date]:
        if not self.is_date(): raise TypeError("Type is not DATE.")
        if self.is_none(): return None
        return self.__value
    def get_time(self) -> Optional[time]:
        if not self.is_time(): raise TypeError("Type is not TIME.")
        if self.is_none(): return None
        return self.__value
    def get_datetime(self) -> Optional[datetime]:
        if not self.is_datetime(): raise TypeError("Type is not DATETIME.")
        if self.is_none(): return None
        return self.__value
    def get_binary(self) -> bytes:
        if not self.is_binary(): raise TypeError("Type is not BINARY.")
        if self.is_none(): return bytes([])
        return self.__value
    def get_string(self) -> str:
        if not self.is_string(): raise TypeError("Type is not STRING.")
        if self.is_none(): return ""
        return self.__value
    def get_list(self) -> list:
        if not self.is_list(): raise TypeError("Type is not LIST.")
        if self.is_none(): return []
        return self.__value
    def get_dict(self) -> dict:
        if not self.is_dict(): raise TypeError("Type is not DICT"
                                                     ".")
        if self.is_none(): return {}
        return self.__value

    def __set__(self, value):

        # Exact type matching
        exact_matches = [
            (lambda v: isinstance(v, bool), lambda: self.is_boolean()),
            (lambda v: isinstance(v, Decimal), lambda: self.is_decimal()),
            (lambda v: isinstance(v, int), lambda: self.is_integer()),
            (lambda v: isinstance(v, float), lambda: self.is_float()),
            (lambda v: isinstance(v, complex), lambda: self.is_complex()),
            (lambda v: isinstance(v, date), lambda: self.is_date()),
            (lambda v: isinstance(v, time), lambda: self.is_time()),
            (lambda v: isinstance(v, datetime), lambda: self.is_datetime()),
            (lambda v: isinstance(v, (bytes, bytearray)), lambda: self.is_binary()),
            (lambda v: isinstance(v, str), lambda: self.is_string()),
            (lambda v: isinstance(v, list), lambda: self.is_list()),
            (lambda v: isinstance(v, dict), lambda: self.is_dict())
        ]
        for value_type, self_type in exact_matches:
            if value_type(value) and self_type():
                self.__set_value__(value)
                return

        # Compatible numeric type matching
        if isinstance(value, (Decimal, int, float, complex)) and self.is_numeric():
            if self.is_decimal():
                if isinstance(value, complex):
                    self.__set_value__(Decimal(value.real));
                    return
            pass

        raise TypeError("Argument type does not match this value type")

    def __set_value__(self, value):
        self.value = value
        self.__modified = True

    def compare_to(self, other) -> int:
        if self.__eq__(other): return 0
        if self.__lt__(other): return -1
        return 1
    def is_comparable(self, other) -> bool:
        if isinstance(other, Value):
            if self.is_numeric() and other.is_numeric(): return True
            if self.__type == other.__type: return True
            return False
        if self.is_boolean(): return isinstance(other, bool)
        if self.is_numeric(): return isinstance(other, (int, float, complex, Decimal))
        if self.is_date(): return isinstance(other, date)
        if self.is_time(): return isinstance(other, time)
        if self.is_datetime(): return isinstance(other, datetime)
        if self.is_binary(): return isinstance(other, bytes)
        if self.is_string(): return isinstance(other, str)
        if self.is_list(): return isinstance(other, list)
        if self.is_dict(): return isinstance(other, dict)
        return False

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
    def __str__(self) -> str: return str(self.__value)
    def __repr__(self):
        if self.is_string(): return "'" + str(self.__value) + "'"
        return self.__str__()
