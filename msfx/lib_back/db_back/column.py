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

from msfx.lib_back.db import (
    BOOLEAN,INTEGER, FLOAT, COMPLEX, DECIMAL, STRING, DATE, TIME, DATETIME, BINARY, OBJECT
)
from msfx.lib_back.dn import (
    Schema, create_from_kwargs, create_from_schema,
    get_string, put_string,
    get_integer, put_integer,
    get_bool, put_bool,
    get_list, get_dict,
    dumps, loads,
    register_class
)
from msfx.lib_back import error_msg

class Column:
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

    schema = Schema()
    schema.add(key=NAME, value_type=str, default_value="")
    schema.add(key=ALIAS, value_type=str, default_value="")
    schema.add(key=TYPE, value_type=str, default_value=STRING)
    schema.add(key=LENGTH, value_type=int, default_value=-1)
    schema.add(key=DECIMALS, value_type=int, default_value=-1)
    schema.add(key=PRIMARY_KEY, value_type=bool, default_value=False)
    schema.add(key=NULLABLE, value_type=bool, default_value=False)
    schema.add(key=UPPERCASE, value_type=bool, default_value=False)
    schema.add(key=HEADER, value_type=str, default_value="")
    schema.add(key=LABEL, value_type=str, default_value="")
    schema.add(key=DESCRIPTION, value_type=str, default_value="")

    def __init__(self, column=None, **kwargs):
        self.__data = {}
        if column is not None and isinstance(column, Column):
            self.__data |= column.__data
        if column is not None and isinstance(column, dict):
            self.__data |= column
        self.__data |= create_from_kwargs(Column.schema, **kwargs)

    def get_name(self) -> str: return get_string(self.__data, Column.NAME)
    def set_name(self, name: str): put_string(self.__data, Column.NAME, name)

    def get_alias(self) -> str:
        alias = get_string(self.__data, Column.ALIAS)
        return alias if len(alias) > 0 else self.get_name()
    def set_alias(self, alias: str): put_string(self.__data, Column.ALIAS, alias)

    def get_type(self) -> str: return get_string(self.__data, Column.TYPE)
    def set_type(self, type: str): put_string(self.__data, Column.TYPE, type)

    def get_length(self) -> int: return get_integer(self.__data, Column.LENGTH)
    def set_length(self, length: int): put_integer(self.__data, Column.LENGTH, length)

    def get_decimals(self) -> int: return get_integer(self.__data, Column.DECIMALS)
    def set_decimals(self, decimals: int): put_integer(self.__data, Column.DECIMALS, decimals)

    def is_primary_key(self) -> bool: return get_bool(self.__data, Column.PRIMARY_KEY)
    def set_primary_key(self, primary_key: bool): put_bool(self.__data, Column.PRIMARY_KEY, primary_key)

    def is_nullable(self) -> bool: return get_bool(self.__data, Column.NULLABLE)
    def set_nullable(self, nullable: bool): put_bool(self.__data, Column.NULLABLE, nullable)

    def is_uppercase(self) -> bool: return get_bool(self.__data, Column.UPPERCASE)
    def set_uppercase(self, uppercase: bool): put_bool(self.__data, Column.UPPERCASE, uppercase)

    def get_header(self) -> str: return get_string(self.__data, Column.HEADER)
    def set_header(self, header: str): put_string(self.__data, Column.HEADER, header)

    def get_label(self) -> str: return get_string(self.__data, Column.LABEL)
    def set_label(self, label: str): put_string(self.__data, Column.LABEL, label)

    def get_description(self) -> str: return get_string(self.__data, Column.DESCRIPTION)
    def set_description(self, description: str): put_string(self.__data, Column.DESCRIPTION, description)

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

    def to_string(self, **kwargs) -> str: return dumps(self.__data, **kwargs)
    def from_string(self, data: str): self.__data = loads(data)
    def to_dict(self) -> dict: return dict(self.__data)

    def __str__(self) -> str: return str(self.__data)
    def __repr__(self): return self.__str__()
    def __iter__(self): return self.__data.__iter__()
    def __len__(self) -> int:  return len(self.__data)

class ColumnList:
    """ An ordered list of columns that can be efficiently accessed either by index or alias. """

    COLUMNS = "columns"
    ALIASES = "aliases"
    INDEXES = "indexes"
    PK_COLUMNS = "pk_columns"
    DEFAULT_VALUES = "default_values"

    schema = Schema()
    schema.add(key=COLUMNS, value_type=list, default_value=[])
    schema.add(key=ALIASES, value_type=list, default_value=[])
    schema.add(key=INDEXES, value_type=dict, default_value={})
    schema.add(key=PK_COLUMNS, value_type=list, default_value=[])
    schema.add(key=DEFAULT_VALUES, value_type=list, default_value=[])

    def __init__(self, column_list=None):
        self.__data =  create_from_schema(ColumnList.schema)
        if column_list is not None and isinstance(column_list, ColumnList):
            self.__data |= column_list.__data
        if column_list is not None and isinstance(column_list, dict):
            self.__data |= column_list

    def append(self, column: Column):
        if column is None or not isinstance(column, Column):
            error = error_msg("type error", "column", type(column), (Column,))
            raise TypeError(error)
        columns = get_list(self.__data, ColumnList.COLUMNS)
        columns.append(column)
        self.__setup()

    def remove(self, key: (int, str)):
        if key is None or not isinstance(key, (int, str)):
            error = error_msg("type error", "key", type(key), (int, str))
            raise TypeError(error)
        index = -1
        if isinstance(key, int): index = key
        if isinstance(key, str): index = self.index_of(key)
        columns = get_list(self.__data, ColumnList.COLUMNS)
        if 0 <= index < len(columns):
            del columns[index]
            self.__setup()

    def clear(self):
        columns = get_list(self.__data, ColumnList.COLUMNS)
        columns.clear()
        self.__setup()

    def index_of(self, alias: str) -> int:
        if alias is None or not isinstance(alias, str):
            error = error_msg("type error", "alias", type(alias), (str,))
            raise TypeError(error)
        indexes = get_dict(self.__data, ColumnList.INDEXES)
        index = indexes.get(alias)
        return -1 if index is None else index

    def get_by_alias(self, alias: str) -> Column:
        if alias is None or not isinstance(alias, str):
            error = error_msg("type error", "alias", type(alias), (str,))
            raise TypeError(error)
        index = self.index_of(alias)
        if index < 0: raise ValueError(f"Invalid alias {alias}")
        columns = get_list(self.__data, ColumnList.COLUMNS)
        return columns[index]

    def get_by_index(self, index: int) -> Column:
        if index is None or not isinstance(index, int):
            error = error_msg("type error", "index", type(index), (int,))
            raise TypeError(error)
        columns = get_list(self.__data, ColumnList.COLUMNS)
        if index < 0:
            error = error_msg("value error", "index", "< 0", (">= 0",))
            raise ValueError(error)
        if index >= len(columns):
            error = error_msg("value error", "index", ">= len(columns)", ("< len(columns)",))
            raise ValueError(error)
        return columns[index]

    def columns(self) -> list:
        columns = get_list(self.__data, ColumnList.COLUMNS)
        return list(columns)
    def aliases(self) -> list:
        aliases = get_list(self.__data, ColumnList.ALIASES)
        return list(aliases)
    def pk_columns(self) -> list:
        pk_aliases = get_list(self.__data, ColumnList.PK_COLUMNS)
        pk_columns = []
        for alias in pk_aliases:
            pk_columns.append(self.get_by_alias(alias))
        return pk_columns
    def default_values(self) -> list:
        default_values = get_list(self.__data, ColumnList.DEFAULT_VALUES)
        return list(default_values)

    def __setup(self):

        columns = get_list(self.__data, ColumnList.COLUMNS)

        aliases = get_list(self.__data, ColumnList.ALIASES)
        indexes = get_dict(self.__data, ColumnList.INDEXES)
        pk_columns = get_list(self.__data, ColumnList.PK_COLUMNS)
        default_values = get_list(self.__data, ColumnList.DEFAULT_VALUES)

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

    def to_string(self, **kwargs) -> str: return dumps(self.__data, **kwargs)
    def from_string(self, data: str): self.__data = loads(data)
    def to_dict(self) -> dict: return dict(self.__data)

    def __str__(self) -> str: return str(self.__data)
    def __repr__(self): return self.__str__()

    def __iter__(self):
        columns = get_list(self.__data, ColumnList.COLUMNS)
        return columns.__iter__()
    def __len__(self) -> int:
        columns = get_list(self.__data, ColumnList.COLUMNS)
        return len(columns)
    def __getitem__(self, index: int) -> Column:
        return self.get_by_index(index)

register_class("column", Column)
register_class("columns", ColumnList)
