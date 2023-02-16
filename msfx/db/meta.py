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
"""
The meta module packs the metadata definitions.
"""

import json
from enum import Enum, EnumMeta
from decimal import Decimal
from datetime import date, time, datetime

class Types(Enum, metaclass=EnumMeta):
    """	Supported types mapped to the underlying SQL databases. """
    BOOLEAN = 0
    """
    A boolean value that is supported in the database either by a BIT
    type or a Y/N or T/F single byte string.
    """
    DECIMAL = 10
    """ A numeric value with fixed number of decimal places. """
    INTEGER = 11
    """ A numeric integer or long value. """
    FLOAT = 13
    """ A numeric double (float) value. """
    COMPLEX = 14
    """ A numeric complex value. """
    DATE = 20
    """ A date value with ISO format '2022-12-21' """
    TIME = 21
    """ A time value with ISO format '10:25:05.135000000' """
    DATETIME = 22
    """ A date-time value with ISO format '2022-12-21T10:25:05.135000000' """
    BINARY = 30
    """
    A binary value, stored in the underlying database in fields of types
    for instance TINYBLOB, BLOB, MEDIUMBLOB or LONGBLOB depending on the length.
    """
    STRING = 40
    """
    A string value, stored in the underlying database in fields of types
    for instance VARCHAR, TINYTEXT, TEXT, MEDIUMTEXT or LONGTEXT depending on the length. 
    """
    JSON = 50
    """
    A JSON object value, stored in the underlying database as a STRING.
    """

class JSON:
    """ JSON value encapsulation. """
    def __init__(self) -> None:
        """ Creates an empty JSON object."""
        self.__data: dict = {}
    def __init(self, json_data) -> None:
        """ Creates a JSON object dumping json string data. """
        self.__data: dict = json.loads(json_data)
    def loads(self, json_data) -> None:
        """ Loads the argument json_data string and merges it with this JSON internal dictionary data. """
        self.__data |= json.loads(json_data)
    def dumps(self) -> str:
        """ Dumps the internal dictionary data and returns a json string representation. """
        return json.dumps(self.__data)
    def merge(self, data: dict) -> None:
        """ Merges the argument dictionary data with this JSON internal dictionary data. """
        if type(data) is not dict: raise "Data to merge must be of dict type"
        self.__data |= data
    def data(self) -> dict:
        """ Gives access to the internal Python data dictionary. """
        return self.__data
    def __str__(self) -> str:
        return str(self.__data)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, JSON):
            return self.__data == other.__data
        if isinstance(other, dict):
            return self.__data == other
        return super().__eq__(other)

class Value:
    """
    A value encapsulates a reference to one of the supported types. Except for the JSON type,
    which internally is a dictionary, the rest of value type can be considered immutable.
    """
    def __init__(self, value):
        """
        Constructs a Value with one of the supported types.
        :param value: The data value or the Types type and the internal value will be None.
        """

        # Argument value can not be None.
        if value is None:
            raise Exception("Argument value can not be None.")

        self.__value = None
        self.__type = None

        # The type is passed as argument value is None, and we are done.
        if isinstance(value, Types): self.__type = value; return

        # Assing the proper type or raise an exception if not supported.
        if isinstance(value, bool): self.__type = Types.BOOLEAN
        elif isinstance(value, Decimal): self.__type = Types.DECIMAL
        elif isinstance(value, int): self.__type = Types.INTEGER
        elif isinstance(value, float): self.__type = Types.FLOAT
        elif isinstance(value, complex): self.__type = Types.COMPLEX
        elif isinstance(value, date): self.__type = Types.DATE
        elif isinstance(value, time): self.__type = Types.TIME
        elif isinstance(value, datetime): self.__type = Types.DATETIME
        elif isinstance(value, bytes): self.__type = Types.BINARY
        elif isinstance(value, str): self.__type = Types.STRING
        elif isinstance(value, JSON): self.__type = Types.JSON
        else: raise Exception(f"Invalid type for argument value: {type(value)}")

        # Assign the value.
        self.__value = value

    def type(self) -> Types: return self.__type
    def value(self) -> object: return self.__value

    def is_none(self) -> bool: return self.__value is None
    def is_boolean(self) -> bool: return self.__type == Types.BOOLEAN
    def is_decimal(self) -> bool: return self.__type == Types.DECIMAL
    def is_integer(self) -> bool: return self.__type == Types.INTEGER
    def is_float(self) -> bool: return self.__type == Types.FLOAT
    def is_complex(self) -> bool: return self.__type == Types.COMPLEX
    def is_date(self) -> bool: return self.__type == Types.DATE
    def is_time(self) -> bool: return self.__type == Types.TIME
    def is_datetime(self) -> bool: return self.__type == Types.DATETIME
    def is_binary(self) -> bool: return self.__type == Types.BINARY
    def is_string(self) -> bool: return self.__type == Types.STRING
    def is_JSON(self) -> bool: return self.__type == Types.JSON

    def is_numeric(self) -> bool:
        if (self.__type == Types.DECIMAL or
            self.__type == Types.INTEGER or
            self.__type == Types.FLOAT or
            self.__type == Types.COMPLEX):
            return True
        return False

    def get_boolean(self) -> bool:
        if not self.is_boolean(): raise Exception("Type is not BOOLEAN")
        if self.is_none(): return False
        return bool(self.__value)

    def get_decimal(self) -> Decimal:
        if not self.is_numeric(): raise Exception("Type is not NUMERIC")
        if self.is_none(): return Decimal(0)
        return Decimal(self.__value)

    def get_integer(self) -> int:
        if not self.is_numeric(): raise Exception("Type is not NUMERIC")
        if self.is_none(): return 0
        return int(self.__value)

    def get_float(self) -> float:
        if not self.is_numeric(): raise Exception("Type is not NUMERIC")
        if self.is_none(): return 0.0
        return float(self.__value)

    def get_complex(self) -> complex:
        if not self.is_numeric(): raise Exception("Type is not NUMERIC")
        if self.is_none(): return complex(0)
        return complex(self.__value)

    def get_date(self) -> date or None:
        if not self.is_date(): raise Exception("Type is not DATE.")
        if self.is_none(): return None
        return self.__value

    def get_time(self) -> time or None:
        if not self.is_time(): raise Exception("Type is not TIME.")
        if self.is_none(): return None
        return self.__value

    def get_datetime(self) -> datetime or None:
        if not self.is_datetime(): raise Exception("Type is not DATETIME.")
        if self.is_none(): return None
        return self.__value

    def get_binary(self) -> bytes:
        if not self.is_binary(): raise Exception("Type is not BINARY.")
        if self.is_none(): return bytes([])
        return self.__value

    def get_string(self) -> str:
        if not self.is_string(): raise Exception("Type is not STRING.")
        if self.is_none(): return ""
        return self.__value

    def get_JSON(self) -> JSON:
        if not self.is_JSON(): raise Exception("Type is not JSON.")
        if self.is_none(): return JSON()
        return self.__value

    def __lt__(self, other: object) -> bool:
        return super().__lt__(other)

    def __le__(self, other: object) -> bool:
        return super().__le__(other)

    def __eq__(self, other: object) -> bool:
        # Other is a Value.
        if isinstance(other, Value):
            return self.__value == other.__value
        # Other is comparable.
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
        if comparable:
            return self.__value == other
        return False

    def __ne__(self, other: object) -> bool:
        return super().__ne__(other)

    def __gt__(self, other: object) -> bool:
        return super().__gt__(other)

    def __ge__(self, other: object) -> bool:
        return super().__ge__(other)

    def __str__(self) -> str:
        if self.is_none(): return ""
        return str(self.__value)
