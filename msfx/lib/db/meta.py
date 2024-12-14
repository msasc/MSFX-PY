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
import copy

from msfx.lib import (
    get_string, put_string, get_integer, put_integer, get_bool, put_bool, get_any, put_any, get_dict, put_dict,
    validate_keys
)
from msfx.lib.db import Types, Value

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
class IndexKeys(Enum):
    """ Keys of the index metadata. """
    NAME = "NAME"
    DESCRIPTION = "DESCRIPTION"
    UNIQUE = "UNIQUE"
    TABLE = "TABLE"
    SEGMENTS = "SEGMENTS"
    # End IndexKeys
class Column:
    """ Column metadata. """

    def __init__(self, column: dict):
        self.__data = None
        if column is not None and isinstance(column, dict):
            validate_keys(column, ColumnKeys, "column")
            self.__data = copy.deepcopy(column)
        if self.__data is None: self.__data = {}

        # Initialize properties
        if self.__data.get(ColumnKeys.PROPERTIES) is None: self.__data[ColumnKeys.PROPERTIES] = {}

    def data(self) -> dict:
        """
        Gives access to the internal data structure. It is necessary to pass the structure
        among several components.
        :return: The internal data structure.
        """
        return self.__data

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
            self.__data = copy.deepcopy(column_list)
        if self.__data is None: self.__data = {}

        # Initialize members not initialized
        if self.__data[ColumnListKeys.COLUMNS] is None: self.__data[ColumnListKeys.COLUMNS] = []
        if self.__data[ColumnListKeys.ALIASES] is None: self.__data[ColumnListKeys.ALIASES] = []
        if self.__data[ColumnListKeys.INDEXES] is None: self.__data[ColumnListKeys.INDEXES] = {}
        if self.__data[ColumnListKeys.PK_COLUMNS] is None: self.__data[ColumnListKeys.PK_COLUMNS] = []
        if self.__data[ColumnListKeys.DEFAULT_VALUES] is None: self.__data[ColumnListKeys.DEFAULT_VALUES] = []

    @property
    def __columns(self) -> list: return self.__data[ColumnListKeys.COLUMNS]
    @property
    def __aliases(self) -> list: return self.__data[ColumnListKeys.ALIASES]
    @property
    def __indexes(self) -> dict: return self.__data[ColumnListKeys.INDEXES]
    @property
    def __pk_columns(self) -> list: return self.__data[ColumnListKeys.PK_COLUMNS]
    @property
    def __default_values(self) -> list: return self.__data[ColumnListKeys.DEFAULT_VALUES]

    def append(self, column: Column):
        if column is None or not isinstance(column, Column):
            raise TypeError("Argument column must be of type Column")
        self.__columns.append(column)
        self.__setup__()

    def remove(self, key: (int, str)):
        if key is None or not isinstance(key, (int, str)):
            raise TypeError("Argument key must be of type int or str")
        index = -1
        if isinstance(key, int): index = key
        if isinstance(key, str): index = self.index_of(key)
        if 0 <= index < len(self.__columns):
            del self.__columns[index]
            self.__setup__()

    def clear(self):
        self.__columns.clear()
        self.__setup__()

    def index_of(self, alias: str) -> int:
        if alias is None or not isinstance(alias, str):
            raise TypeError("Argument alias must be of type str")
        index = self.__indexes.get(alias)
        return -1 if index is None else index

    def get_by_alias(self, alias: str) -> Column:
        if alias is None or not isinstance(alias, str):
            raise TypeError("Argument alias must be of type str")
        index = self.index_of(alias)
        if index < 0: raise ValueError(f"Invalid alias {alias}")
        return self.__columns[index]

    def get_by_index(self, index: int) -> Column:
        if index is None or not isinstance(index, int): raise TypeError("")
        if index < 0: raise ValueError("")
        if index >= len(self.__columns): raise ValueError("Index out of range")
        return self.__columns[index]

    def columns(self) -> list: return list(self.__columns)
    def aliases(self) -> list: return list(self.__aliases)
    def pk_columns(self) -> list: return list(self.__pk_columns)
    def default_values(self) -> list: return list(self.__default_values)

    def __setup__(self):

        for i in range(len(self.__columns)):
            column: Column = self.__columns[i]
            alias: str = column.get_alias()
            self.__aliases.append(alias)
            self.__indexes[alias] = i
            if column.is_primary_key():
                self.__pk_columns.append(column)
            self.__default_values.append(column.get_default_value())

    # End ColumnList
class Index:
    """ Index metadata. Can be used as an index of a table or as a simple order. """
    pass
