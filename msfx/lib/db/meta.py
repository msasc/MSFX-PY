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

from enum import Enum
from typing import Optional

from msfx.lib import round_dec
from msfx.lib.db import Types, Value
from msfx.lib.props import Properties

class ColumnKeys(Enum):
    NAME = "NAME"
    ALIAS = "ALIAS"
    TYPE = "TYPE"
    LENGTH = "LENGTH"
    SCALE = "SCALE"
    PRIMARY_KEY = "PRIMARY_KEY"
    NULLABLE = "NULLABLE"
    UPPERCASE = "UPPERCASE"
    HEADER = "HEADER"
    LABEL = "LABEL"
    DESCRIPTION = "DESCRIPTION"
    TABLE = "TABLE"
    VIEW = "VIEW"
    PROPERTIES = "PROPERTIES"
class ColumnListKeys(Enum):
    COLUMNS = "COLUMNS"
    ALIASES = "ALIASES"
    INDEXES = "INDEXES"
    PK_COLUMNS = "PK_COLUMNS"
    DEFAULT_VALUES = "DEFAULT_VALUES"
class OrderKeys(Enum):
    SEGMENTS = "SEGMENTS"

class Column:
    """ Column metadata. """

    def __init__(self, **kwargs):
        self.__props = Properties()

        # Extra properties initialized so directly can be used.
        self.__props.set_props(ColumnKeys.PROPERTIES, Properties())

    def get_name(self) -> str: return self.__props.get_string(ColumnKeys.NAME)
    def get_alias(self) -> str:
        alias = self.__props.get_string(ColumnKeys.ALIAS)
        if len(alias) == 0: alias = self.get_name()
        return alias
    def get_type(self) -> Types: return self.__props.get_any(ColumnKeys.TYPE, Types.STRING)
    def get_length(self) -> int: return self.__props.get_integer(ColumnKeys.LENGTH, -1)
    def get_scale(self) -> int: return self.__props.get_integer(ColumnKeys.SCALE, -1)

    def is_primary_key(self) -> bool: return self.__props.get_bool(ColumnKeys.PRIMARY_KEY, False)
    def is_nullable(self) -> bool: return self.__props.get_bool(ColumnKeys.NULLABLE, True)
    def is_uppercase(self) -> bool: return self.__props.get_bool(ColumnKeys.UPPERCASE, False)

    def get_header(self) -> str: return self.__props.get_string(ColumnKeys.HEADER)
    def get_label(self) -> str: return self.__props.get_string(ColumnKeys.LABEL)
    def get_description(self) -> str: return self.__props.get_string(ColumnKeys.DESCRIPTION)

    # To avoid circular references, table and view store their properties
    def get_table_props(self) -> Optional[Properties]: return self.__props.get_props(ColumnKeys.TABLE)
    def get_view_props(self) -> Optional[Properties]: return self.__props.get_props(ColumnKeys.VIEW)

    def get_props(self) -> Properties: return self.__props.get_props(ColumnKeys.PROPERTIES)

    def get_default_value(self) -> Value:
        type: Types = self.get_type()
        scale: int = self.get_scale()
        if type == Types.BOOLEAN: return Value(False)
        if type == Types.DECIMAL: return Value(round_dec(0, scale))
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

    def set_name(self, name: str): self.__props.set_string(ColumnKeys.NAME, name)
    def set_alias(self, alias: str): self.__props.set_string(ColumnKeys.ALIAS, alias)
    def set_type(self, type: Types): self.__props.set_any(ColumnKeys.TYPE, type)
    def set_length(self, length: int): self.__props.set_integer(ColumnKeys.LENGTH, length)
    def set_scale(self, scale: int): self.__props.set_integer(ColumnKeys.SCALE, scale)

    def set_primary_key(self, primary_key: bool): self.__props.set_bool(ColumnKeys.PRIMARY_KEY, False)
    def set_nullable(self, nullable: bool): self.__props.set_bool(ColumnKeys.NULLABLE, True)
    def set_uppercase(self, uppercase: bool): self.__props.set_bool(ColumnKeys.UPPERCASE, False)

    def set_header(self, header: str): self.__props.set_string(ColumnKeys.HEADER, header)
    def set_label(self, label: str): self.__props.set_string(ColumnKeys.LABEL, label)
    def set_description(self, description: str): self.__props.set_string(ColumnKeys.DESCRIPTION, description)

    def set_table_props(self, props: Properties): self.__props.set_props(ColumnKeys.TABLE, props)
    def set_view_props(self, props: Properties): self.__props.set_props(ColumnKeys.VIEW, props)

    def __str__(self) -> str:
        col = "[\""
        col += self.get_name()
        col += "\", \""
        col += self.get_type().name
        col += "\", "
        if self.get_length() >= 0: col += str(self.get_length())
        else: col += "--"
        col += ", "
        if self.get_scale() >= 0: col += str(self.get_scale())
        else: col += "--"
        col += ", \""
        col += self.get_header()
        col += "\"]"
        return col
    def __repr__(self): return self.__str__()
    """ End of class Column """
class ColumnList:
    """ Column list metadata. """
    def __init__(self):
        self.__props = Properties()
        self.__props.set_list(ColumnListKeys.COLUMNS, [])
        self.__props.set_list(ColumnListKeys.ALIASES, [])
        self.__props.set_dict(ColumnListKeys.INDEXES, {})
        self.__props.set_list(ColumnListKeys.PK_COLUMNS, [])
        self.__props.set_list(ColumnListKeys.DEFAULT_VALUES, [])

    @property
    def __columns(self) -> list: return self.__props.get_list(ColumnListKeys.COLUMNS)
    @property
    def __aliases(self) -> list: return self.__props.get_list(ColumnListKeys.ALIASES)
    @property
    def __indexes(self) -> dict: return self.__props.get_dict(ColumnListKeys.INDEXES)
    @property
    def __pk_columns(self) -> list: return self.__props.get_list(ColumnListKeys.PK_COLUMNS)
    @property
    def __default_values(self) -> list: return self.__props.get_list(ColumnListKeys.DEFAULT_VALUES)

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

        self.__aliases.clear()
        self.__indexes.clear()
        self.__pk_columns.clear()
        self.__default_values.clear()

        for i in range(len(self.__columns)):
            column: Column = self.__columns[i]
            self.__aliases.append(column.get_alias())
            self.__indexes[column.get_alias()] = i
            if column.is_primary_key():
                self.__pk_columns.append(column)
            self.__default_values.append(column.get_default_value())
    """ End of class ColumnList """
class Order:
    """ An order definition. """
    def __init__(self):
        self.__props = Properties()
        self.__props.set_list(OrderKeys.SEGMENTS, [])

    def append(self, column: Column, ascending: bool = True):
        if column is None or not isinstance(column, Column):
            raise TypeError("Argument column must be of type Column")