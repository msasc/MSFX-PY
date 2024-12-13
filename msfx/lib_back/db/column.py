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
from decimal import Decimal

from msfx.lib_back import Data, create_from_kwargs, get_string, put_string, get_integer, put_integer, get_bool, put_bool, \
    register_class, merge_dicts, check_type, check_value
from msfx.lib_back.db import BOOLEAN, INTEGER, FLOAT, COMPLEX, DECIMAL, STRING, DATE, TIME, DATETIME, BINARY, OBJECT

class Column(Data):
    """ A column definition. """

    NAME = "name"
    ALIAS = "alias"
    TYPE = "type"
    LENGTH = "length"
    DECIMALS = "decimals"
    PRIMARY_KEY = "primary_key"
    NULLABLE = "nullable"
    UPPERCASE = "uppercase"
    HEADER = "header"
    LABEL = "label"
    DESCRIPTION = "description"

    KEYS = [
        NAME, ALIAS, TYPE, LENGTH, DECIMALS,
        PRIMARY_KEY, NULLABLE, UPPERCASE,
        HEADER, LABEL, DESCRIPTION
    ]

    def __init__(self, column=None, **kwargs):
        super().__init__()
        self._data = {}
        if column is not None and isinstance(column, Column):
            self.from_dict(column._data)
        if column is not None and isinstance(column, dict):
            self.from_dict(column)
        self._data = create_from_kwargs(Column.KEYS, **kwargs)

    def get_name(self) -> str: return get_string(self._data, Column.NAME)
    def set_name(self, name: str): put_string(self._data, Column.NAME, name)

    def get_alias(self) -> str:
        alias = get_string(self._data, Column.ALIAS)
        return alias if len(alias) > 0 else self.get_name()
    def set_alias(self, alias: str): put_string(self._data, Column.ALIAS, alias)

    def get_type(self) -> str: return get_string(self._data, Column.TYPE)
    def set_type(self, type: str): put_string(self._data, Column.TYPE, type)

    def get_length(self) -> int: return get_integer(self._data, Column.LENGTH)
    def set_length(self, length: int): put_integer(self._data, Column.LENGTH, length)

    def get_decimals(self) -> int: return get_integer(self._data, Column.DECIMALS)
    def set_decimals(self, decimals: int): put_integer(self._data, Column.DECIMALS, decimals)

    def is_primary_key(self) -> bool: return get_bool(self._data, Column.PRIMARY_KEY)
    def set_primary_key(self, primary_key: bool): put_bool(self._data, Column.PRIMARY_KEY, primary_key)

    def is_nullable(self) -> bool: return get_bool(self._data, Column.NULLABLE)
    def set_nullable(self, nullable: bool): put_bool(self._data, Column.NULLABLE, nullable)

    def is_uppercase(self) -> bool: return get_bool(self._data, Column.UPPERCASE)
    def set_uppercase(self, uppercase: bool): put_bool(self._data, Column.UPPERCASE, uppercase)

    def get_header(self) -> str: return get_string(self._data, Column.HEADER)
    def set_header(self, header: str): put_string(self._data, Column.HEADER, header)

    def get_label(self) -> str: return get_string(self._data, Column.LABEL)
    def set_label(self, label: str): put_string(self._data, Column.LABEL, label)

    def get_description(self) -> str: return get_string(self._data, Column.DESCRIPTION)
    def set_description(self, description: str): put_string(self._data, Column.DESCRIPTION, description)

    def get_default_value(self) -> object:
        column_type = self.get_type()
        if column_type == BOOLEAN: return False
        if column_type == INTEGER: return 0
        if column_type == FLOAT: return 0.0
        if column_type == COMPLEX: return complex(0)
        if column_type == DECIMAL:
            decimals = self.get_decimals()
            return Decimal() if decimals <= 0 else round(Decimal(), decimals)
        if column_type == STRING: return ""
        if column_type in (DATE, TIME, DATETIME): return None
        if column_type == BINARY: return None
        if column_type == OBJECT: return {}

    def from_dict(self, data: dict):
        merge_dicts(data, self._data, Column.KEYS)

register_class("column", Column)

class ColumnList(Data):
    """ An ordered list of columns that can be efficiently accessed either by index or alias. """

    COLUMNS = "columns"
    ALIASES = "aliases"
    INDEXES = "indexes"
    PK_COLUMNS = "pk_columns"
    DEFAULT_VALUES = "default_values"

    KEYS = [COLUMNS, ALIASES, INDEXES, PK_COLUMNS, DEFAULT_VALUES]

    def __init__(self, column_list=None):
        super().__init__()
        self._data = {
            ColumnList.COLUMNS: [],
            ColumnList.ALIASES: [],
            ColumnList.INDEXES: {},
            ColumnList.PK_COLUMNS: [],
            ColumnList.DEFAULT_VALUES: []
        }
        if column_list is not None and isinstance(column_list, ColumnList):
            self.from_dict(column_list._data)
        if column_list is not None and isinstance(column_list, dict):
            self.from_dict(column_list)

    def append(self, column: Column):
        self._data[ColumnList.COLUMNS].append(column)
        self.__setup()

    def clear(self):
        self._data[ColumnList.COLUMNS].clear()
        self.__setup()

    def index_of(self, alias: str) -> int:
        check_type("alias", type(alias), (str,))
        index = self._data[ColumnList.INDEXES].get(alias)
        return -1 if index is None else index

    def get_by_alias(self, alias: str) -> Column:
        check_type("alias", type(alias), (str,))
        index = self.index_of(alias)
        if index < 0: raise ValueError(f"Invalid alias {alias}")
        return self._data[ColumnList.COLUMNS][index]

    def get_by_index(self, index: int) -> Column:
        check_type("index", type(index), (int,))
        check_value("index", index < 0,"index < 0", ("index >= 0",))
        check_value("index", index >= len(self), "index >= len(columns)", ("index < len(columns)",))
        return self._data[ColumnList.COLUMNS][index]

    def __setup(self):
        columns = self._data[ColumnList.COLUMNS]

        aliases = self._data[ColumnList.ALIASES]
        indexes = self._data[ColumnList.INDEXES]
        pk_columns = self._data[ColumnList.PK_COLUMNS]
        default_values = self._data[ColumnList.DEFAULT_VALUES]

        aliases.clear()
        indexes.clear()
        pk_columns.clear()
        default_values.clear()

        for i in range(len(columns)):
            column: Column = columns[i]
            alias = column.get_alias()
            aliases.append(alias)
            indexes[alias] = i
            if column.is_primary_key():
                pk_columns.append(alias)
            default_values.append(column.get_default_value())

    def from_dict(self, data):
        merge_dicts(data, self._data, ColumnList.KEYS)

    def __iter__(self): return self._data[ColumnList.COLUMNS].__iter__()
    def __len__(self) -> int: return len(self._data[ColumnList.COLUMNS])
    def __getitem__(self, index: int) -> Column: return self.get_by_index(index)

register_class("column-list", ColumnList)
