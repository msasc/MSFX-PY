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

from datetime import date, time, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from numbers import Complex
from typing import Optional, Dict, Any

from msfx.lib import round_num

class Types(Enum):
    """
    Types accepted within this database SQL metadata.

    Boolean values are stored in a VARCHAR(1) column with Y/N for readability,
    although when read (Y/N), (T/F), (1,0) are accepted and empty/NULL is False.
    """
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
    def get_types_none() -> tuple: return Types.DATE, Types.TIME, Types.DATETIME
    @staticmethod
    def get_types_numeric() -> tuple: return Types.INTEGER, Types.FLOAT, Types.DECIMAL, Types.COMPLEX
    @staticmethod
    def get_types_length() -> tuple: return Types.DECIMAL, Types.STRING, Types.BINARY
    @staticmethod
    def get_types_date_time() -> tuple: return Types.DATE, Types.TIME, Types.DATETIME

    def is_numeric(self) -> bool: return self in Types.get_types_numeric()
    def requires_length(self) -> bool: return self in Types.get_types_length()
    def accepts_none(self) -> bool: return self in Types.get_types_none()

    """ End of class Types """
class Value:
    """ Encapsulates a mutable value of one of the supported types. """
    def __init__(self, value):
        # Argument value can not be None: either it is a non None value,
        # or a type which value can be None.
        if value is None: raise TypeError(f"Value can not be {None}.")

        # If value is an instance of Types is must be one of the types
        # that are nullable (DATE, TIME, DATETIME and BINARY).
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

    def type(self) -> Types:
        return self.__type
    def value(self) -> object:
        return self.__value

    def is_modified(self) -> bool:
        return self.__modified

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
    def is_numeric(self) -> bool:
        return self.__type in Types.get_types_numeric()
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
    def is_dict(self) -> bool:
        return self.__type == Types.DICT

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
        return Decimal(self.__value)
    def get_integer(self) -> int:
        if not self.is_numeric():
            raise TypeError("Type is not NUMERIC")
        if self.is_none():
            return 0
        return int(self.__value)
    def get_float(self) -> float:
        if not self.is_numeric():
            raise TypeError("Type is not NUMERIC")
        if self.is_none():
            return 0.0
        return float(self.__value)
    def get_complex(self) -> complex:
        if not self.is_numeric():
            raise TypeError("Type is not NUMERIC")
        if self.is_none():
            return complex(0, 0)
        return complex(self.__value)
    def get_date(self) -> Optional[date]:
        if not self.is_date():
            raise TypeError("Type is not DATE.")
        if self.is_none():
            return None
        return self.__value
    def get_time(self) -> Optional[time]:
        if not self.is_time():
            raise TypeError("Type is not TIME.")
        if self.is_none():
            return None
        return self.__value
    def get_datetime(self) -> Optional[datetime]:
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
    def get_dict(self) -> dict:
        if not self.is_dict():
            raise TypeError("Type is not DICT")
        if self.is_none():
            return {}
        return self.__value

    def get_scale(self) -> int:
        if self.__type not in (Types.DECIMAL, Types.INTEGER):
            raise TypeError("The scale has sense only for DECIMAL and INTEGER types")
        if self.is_none():
            return 0
        if self.is_integer():
            return 0
        return abs(int(self.get_decimal().as_tuple().exponent))

    def set_bool(self, value: bool):
        self.__set__(value)
    def set_decimal(self, value: Decimal):
        self.__set__(value)
    def set_integer(self, value: int):
        self.__set__(value)
    def set_float(self, value: float):
        self.__set__(value)
    def set_complex(self, value: complex):
        self.__set__(value)
    def set_date(self, value: Optional[date]):
        self.__set__(value)
    def set_time(self, value: Optional[time]):
        self.__set__(value)
    def set_datetime(self, value: Optional[datetime]):
        self.__set__(value)
    def set_binary(self, value: (bytes, bytearray)):
        self.__set__(value)
    def set_string(self, value: str):
        self.__set__(value)
    def set_list(self, value: list):
        self.__set__(value)
    def set_dict(self, value: dict):
        self.__set__(value)

    def is_none(self):
        return self.__value is None
    def set_none(self):
        self.__value = None

    def __set__(self, value):
        # The value can not be None in a set operation.
        if value is None:
            if self.__type not in (Types.DATE, Types.TIME, Types.DATETIME):
                raise ValueError("Value can only be None for types DATE, TIME, DATETIME.")

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
                self.__value = value
                self.__modified = True
                return

        # Compatible numeric type matching
        if isinstance(value, (Decimal, int, float, complex)) and self.is_numeric():
            if isinstance(value, complex): value = value.real
            if self.is_decimal():
                # self is decimal and not None, preserve scale
                scale = self.get_scale()
                self.__value = round_num(value, scale)
            else:
                if self.is_integer():
                    self.__value = int(value)
                if self.is_float():
                    self.__value = float(value)
                if self.is_complex():
                    self.__value = complex(value)
            self.__modified = True
            return

        raise TypeError("Argument type does not match this value type")

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
            return isinstance(other, list)
        if self.is_dict():
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
        if self.__value is None:
            return ""
        return str(self.__value)
    def __repr__(self):
        if self.is_string():
            return "'" + str(self.__value) + "'"
        return self.__str__()
    """ End of class Value """
class Key:
    """
    A key or list of tuples of a value and an ascending/descending boolean.
    A key is just aimed to append segments and use it.
    The clear method is there to reuse the key.
    """
    def __init__(self):
        self.__segments = []

    def append(self, value: Value):
        self.__segments.append(value)
    def clear(self):
        self.__segments.clear()

    def __iter__(self):
        return self.__segments.__iter__()
    def __len__(self) -> int:
        return len(self.__segments)
    def __getitem__(self, index: int) -> Value:
        return self.__segments[index]
    def __lt__(self, other) -> bool:
        return self.__segments < other.__segments
    def __le__(self, other) -> bool:
        return self.__segments <= other.__segments
    def __eq__(self, other) -> bool:
        return self.__segments == other.__segments
    def __ne__(self, other) -> bool:
        return not self.__segments == other.__segments
    def __gt__(self, other) -> bool:
        return self.__segments > other.__segments
    def __ge__(self, other) -> bool:
        return self.__segments >= other.__segments
    """ End of class OrderKey """
class OrderKey:
    """
    An order key or list of tuples of a value and an ascending/descending boolean.
    An order key is just aimed to append segments and use it.
    The clear method is there to reuse the key.
    """
    def __init__(self):
        self.__segments = []

    def append(self, value: Value, asc: bool):
        self.__segments.append((value, asc))
    def clear(self):
        self.__segments.clear()

    def __iter__(self):
        return self.__segments.__iter__()
    def __len__(self) -> int:
        return len(self.__segments)
    def __getitem__(self, index: int) -> (Value, bool):
        return self.__segments[index]
    def __lt__(self, other) -> bool:
        return self.__segments < other.__segments
    def __le__(self, other) -> bool:
        return self.__segments <= other.__segments
    def __eq__(self, other) -> bool:
        return self.__segments == other.__segments
    def __ne__(self, other) -> bool:
        return not self.__segments == other.__segments
    def __gt__(self, other) -> bool:
        return self.__segments > other.__segments
    def __ge__(self, other) -> bool:
        return self.__segments >= other.__segments
    """ End of class OrderKey """

TYPE_MAPPING = {
    Types.BOOLEAN: bool,
    Types.DECIMAL: Decimal,
    Types.INTEGER: int,
    Types.FLOAT: float,
    Types.COMPLEX: Complex,
    Types.DATE: date,
    Types.TIME: time,
    Types.DATETIME: datetime,
    Types.BINARY: bytes,
    Types.STRING: str,
    Types.LIST: list,
    Types.DICT: dict,
}

def get_default_value(type: Types, scale: int) -> Value:
    """
    Returns a default value for the given type and optional scale for decimals.
    :param type: The type to get the default value for.
    :param scale: The scale to apply for decimals.
    :return: The default value.
    """
    if type == Types.BOOLEAN: return Value(False)
    if type == Types.DECIMAL: return Value(round_num(0, scale))
    if type == Types.INTEGER: return Value(int(0))
    if type == Types.FLOAT: return Value(float(0))
    if type == Types.COMPLEX: return Value(complex(0))
    if type == Types.DATE: return Value(Types.DATE)
    if type == Types.TIME: return Value(Types.TIME)
    if type == Types.DATETIME: return Value(Types.DATETIME)
    if type == Types.BINARY: return Value(bytes([]))
    if type == Types.STRING: return Value(str(""))
    if type == Types.LIST: return Value(list([]))
    if type == Types.DICT: return Value(dict({}))
    raise ValueError(f"Unsupported type {type}")

def get_value(type: Types, scale: int, raw_value: any) -> Value:
    """
    Returns a value for the given type, optional scale for decimals and a raw value.
    :param type: The type to get the value for.
    :param scale: The scale to apply for decimals.
    :param raw_value: The raw value to use.
    :return: The corresponding value.
    """

    # The type must be correct.
    if not isinstance(type, Types):
        raise TypeError(f"Type {type} is not a Types instance")

    # If the type is DECIMAL then the scale must be GE 0.
    if type == Types.DECIMAL:
        if not isinstance(scale, int) or scale < 0:
            raise ValueError(f"Scale {scale} is not a positive integer")

    # Decimal match, ensure scale.
    if type == Types.DECIMAL and isinstance(raw_value, Decimal):
        return Value(round_num(raw_value, scale))

    # If the raw value is None return the default value for the type.
    if raw_value is None:
        return get_default_value(type, scale)

    # Direct matches
    expected_instance = TYPE_MAPPING.get(type)
    if expected_instance and isinstance(raw_value, expected_instance):
        return Value(raw_value)

    # Conversion of numeric types
    if type == Types.COMPLEX and isinstance(raw_value, (Decimal, int, float)):
        return Value(complex(raw_value))
    if type == Types.DECIMAL and isinstance(raw_value, (int, float)):
        value = Decimal(str(raw_value))
        return Value(round_num(raw_value, scale))
    if type == Types.INTEGER and isinstance(raw_value, (Decimal, float)):
        return Value(int(raw_value))
    if type == Types.FLOAT and isinstance(raw_value, (Decimal, int)):
        return Value(float(raw_value))
    if type.is_numeric() and isinstance(raw_value, complex):
        if type == Types.DECIMAL: return Value(Decimal(raw_value.real))
        if type == Types.INTEGER: return Value(int(raw_value.real))
        if type == Types.FLOAT: return Value(float(raw_value.real))

    # Conversion of time_delta to time.
    if type == Types.TIME and isinstance(raw_value, timedelta):
        time_of_day = (datetime.min + raw_value).time()
        return Value(time_of_day)

    # Conversion on int (time in millis) to datetime
    if type in Types.get_types_date_time() and isinstance(raw_value, int):
        value = datetime.fromtimestamp(raw_value / 1000)
        if type == Types.DATE: return Value(value.date())
        if type == Types.TIME: return Value(value.time())
        if type == Types.DATETIME: return Value(value)

    raise ValueError(f"Unsupported value {raw_value} for type {type}")