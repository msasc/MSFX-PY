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

from enum import Enum, auto
from datetime import date, time, datetime
from decimal import Decimal
from msfx.lib import (
    get_string, put_string, get_integer, put_integer, get_bool, put_bool, get_any, put_any, get_dict, put_dict,
    validate_keys, put_list
)

class Types(Enum):
    """
    Types accepted within this database SQL metadata.

    The adapter of the underlying database engine will be responsible
    for saving/retrieving correctly the value. By default,

    BOOLEAN
        Will be stored in a VARCHAR(1) T/F.
    DECIMAL, INTEGER, FLOAT
        Will be stored in the appropriate numeric types.
    DATE, TIME, DATETIME
        Will be stored in the appropriate datetime types.
    BINARY
        As RAW, BINARY, VARBINARY, BLOB, LOB, depending on the database and the size.
    STRING
        As VARCHAR, CLOB, depending on the database and the size.
    LIST, DICT
        As JSON objects.
    """
    BOOLEAN = "BOOLEAN"
    DECIMAL = "DECIMAL"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
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
    def get_types_numeric() -> tuple: return Types.INTEGER, Types.FLOAT, Types.DECIMAL
    @staticmethod
    def get_types_length() -> tuple: return Types.DECIMAL, Types.STRING, Types.BINARY
    # End Types
class Value:
    """ Encapsulates an immutable value of one of the supported types. """
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
        self.__type = None

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

    def is_none(self) -> bool: return self.__value is None
    def is_boolean(self) -> bool: return self.__type == Types.BOOLEAN
    def is_decimal(self) -> bool: return self.__type == Types.DECIMAL
    def is_integer(self) -> bool: return self.__type == Types.INTEGER
    def is_float(self) -> bool: return self.__type == Types.FLOAT
    def is_date(self) -> bool: return self.__type == Types.DATE
    def is_time(self) -> bool: return self.__type == Types.TIME
    def is_datetime(self) -> bool: return self.__type == Types.DATETIME
    def is_binary(self) -> bool: return self.__type == Types.BINARY
    def is_string(self) -> bool: return self.__type == Types.STRING
    def is_list(self) -> bool: return self.__type == Types.LIST
    def is_dictionary(self) -> bool: return self.__type == Types.DICT

    def is_numeric(self) -> bool: return self.__type in Types.get_types_numeric()
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
    def get_date(self) -> date or None:
        if not self.is_date(): raise TypeError("Type is not DATE.")
        if self.is_none(): return None
        return self.__value
    def get_time(self) -> time or None:
        if not self.is_time(): raise TypeError("Type is not TIME.")
        if self.is_none(): return None
        return self.__value
    def get_datetime(self) -> datetime or None:
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
    def get_dictionary(self) -> dict:
        if not self.is_dictionary(): raise TypeError("Type is not DICTIONARY.")
        if self.is_none(): return {}
        return self.__value

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
        if self.is_dictionary(): return isinstance(other, dict)
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
    # End Value
class ColumnKeys(Enum):
    """ Keys of the column metadata. """

    NAME = "NAME"
    ALIAS = "ALIAS"
    TYPE = "TYPE"
    LENGTH = "LENGTH"
    DECIMALS = "DECIMALS"

    PRIMARY_KEY = "PRIMARY_KEY"
    NULLABLE = "NULLABLE"

    UPPERCASE = "UPPERCASE"
    HEADER = "HEADER"
    LABEL = "LABEL"
    DESCRIPTION = "DESCRIPTION"

    TABLE = "TABLE"
    VIEW = "VIEW"

    PROPERTIES = "PROPERTIES"
    # End ColumnKeys
class ColumnListKeys(Enum):
    """ Keys of the column list metadata. """

    COLUMNS = "COLUMNS"
    ALIASES = "ALIASES"
    INDEXES = "INDEXES"
    PK_COLUMNS = "PK_COLUMNS"
    DEFAULT_VALUES = "DEFAULT_VALUES"
    # End ColumnListkeys
class Column:
    """ Column metadata. """

    def __init__(self, column: dict):
        self.__data = None
        if column is not None and isinstance(column, dict):
            validate_keys(column, ColumnKeys, "column")
            self.__data = column
        if self.__data is None: self.__data = {}

        # Initialize properties
        if self.__data.get(ColumnKeys.PROPERTIES) is None: self.__data[ColumnKeys.PROPERTIES] = {}

    def get_name(self) -> str: return get_string(self.__data, ColumnKeys.NAME)
    def set_name(self, name: str): put_string(self.__data, ColumnKeys.NAME, name)

    def get_alias(self) -> str:
        alias = get_string(self.__data, ColumnKeys.ALIAS)
        return alias if len(alias) > 0 else self.get_name()
    def set_alias(self, alias: str): put_string(self.__data, ColumnKeys.ALIAS, alias)

    def get_type(self) -> Types: return get_any(self.__data, ColumnKeys.TYPE)
    def set_type(self, type: Types): put_any(self.__data, ColumnKeys.TYPE, type)

    def get_length(self) -> int: return get_integer(self.__data, ColumnKeys.LENGTH)
    def set_length(self, length: int): put_integer(self.__data, ColumnKeys.LENGTH, length)

    def get_decimals(self) -> int: return get_integer(self.__data, ColumnKeys.DECIMALS)
    def set_decimals(self, decimals: int): put_integer(self.__data, ColumnKeys.DECIMALS, decimals)

    def is_primary_key(self) -> bool: return get_bool(self.__data, ColumnKeys.PRIMARY_KEY)
    def set_primary_key(self, primary_key: bool): put_bool(self.__data, ColumnKeys.PRIMARY_KEY, primary_key)

    def is_nullable(self) -> bool: return get_bool(self.__data, ColumnKeys.NULLABLE)
    def set_nullable(self, nullable: bool): put_bool(self.__data, ColumnKeys.NULLABLE, nullable)

    def is_uppercase(self) -> bool: return get_bool(self.__data, ColumnKeys.UPPERCASE)
    def set_uppercase(self, uppercase: bool): put_bool(self.__data, ColumnKeys.UPPERCASE, uppercase)

    def get_header(self) -> str: return get_string(self.__data, ColumnKeys.HEADER)
    def set_header(self, header: str): put_string(self.__data, ColumnKeys.HEADER, header)

    def get_label(self) -> str: return get_string(self.__data, ColumnKeys.LABEL)
    def set_label(self, label: str): put_string(self.__data, ColumnKeys.LABEL, label)

    def get_description(self) -> str: return get_string(self.__data, ColumnKeys.DESCRIPTION)
    def set_description(self, description: str): put_string(self.__data, ColumnKeys.DESCRIPTION, description)

    def get_table(self) -> dict: return get_dict(self.__data, ColumnKeys.TABLE)
    def set_table(self, table: dict): put_dict(self.__data, ColumnKeys.TABLE, table)

    def get_view(self) -> dict: return get_dict(self.__data, ColumnKeys.VIEW)
    def set_view(self, view: dict): put_dict(self.__data, ColumnKeys.VIEW, view)

    def get_default_value(self) -> Value:
        type: Types = self.get_type()
        decs: int = self.get_decimals()
        decs = decs if decs >= 0 else 0
        if type == Types.BOOLEAN: return Value(False)
        if type == Types.DECIMAL: return Value(round(Decimal(0), decs))
        if type == Types.INTEGER: return Value(int(0))
        if type == Types.FLOAT: return Value(float(0))
        if type == Types.DATE: return Value(Types.DATE)
        if type == Types.TIME: return Value(Types.TIME)
        if type == Types.DATETIME: return Value(Types.DATETIME)
        if type == Types.BINARY: return Value(bytes([]))
        if type == Types.STRING: return Value(str(""))
        if type == Types.LIST: return Value(list([]))
        if type == Types.DICT: return Value(dict({}))
        raise ValueError(f"Unsupported type {type}")
    # End Column
class ColumnList:
    """ Column list metadata. """
    def __init__(self, column_list: dict):
        self.__data = None
        if column_list is not None and isinstance(column_list, dict):
            validate_keys(column_list, ColumnListKeys, "column list")
            self.__data = column_list
        if self.__data is None: self.__data = {}

        # Initialize members not initialized
        if self.__data[ColumnListKeys.COLUMNS] is None: self.__data[ColumnListKeys.COLUMNS] = []
        if self.__data[ColumnListKeys.ALIASES] is None: self.__data[ColumnListKeys.ALIASES] = []
        if self.__data[ColumnListKeys.INDEXES] is None: self.__data[ColumnListKeys.INDEXES] = {}
        if self.__data[ColumnListKeys.PK_COLUMNS] is None: self.__data[ColumnListKeys.PK_COLUMNS] = []
        if self.__data[ColumnListKeys.DEFAULT_VALUES] is None: self.__data[ColumnListKeys.DEFAULT_VALUES] = []
        # End __init__
    def __setup__(self):
        aliases: list = self.__data[ColumnListKeys.ALIASES]
        indexes: dict = self.__data[ColumnListKeys.INDEXES]
        pk_columns: list = self.__data[ColumnListKeys.PK_COLUMNS]
        default_values: list = self.__data[ColumnListKeys.DEFAULT_VALUES]

        columns: list = self.__data[ColumnListKeys.COLUMNS]

        for i in range(len(columns)):
            column: Column = columns[i]
            alias: str = column.get_alias()
            aliases.append(alias)
            indexes[alias] = i
            if column.is_primary_key():
                pk_columns.append(column)
            default_values.append(column.get_default_value())
    # End ColumnList