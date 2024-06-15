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
from msfx.lib.db.schema import (
    COLUMN_SCHEMA,
    COLUMN_NAME, COLUMN_ALIAS,
    COLUMN_TYPE, COLUMN_LENGTH, COLUMN_DECIMALS,
    COLUMN_PRIMARY_KEY,
    COLUMN_HEADER, COLUMN_LABEL, COLUMN_DESCRIPTION,
    COLUMN_TABLE, COLUMN_VIEW,
    Table, View
)
from msfx.lib.db.types import Types
from msfx.lib.db.value import Value
from msfx.lib.util.generics import dict_get_value, dict_set_value, dict_create_args
from msfx.lib.util.json import dumps

class Column:
    """ A column of a table or view. """
    def __init__(self, column=None, **kwargs):
        self.__data = {}
        if len(kwargs) > 0:
            self.__data = dict_create_args(COLUMN_SCHEMA, **kwargs)
        if isinstance(column, Column):
            self.__data |= column.__data

    def get_name(self) -> str:
        return dict_get_value(self.__data, COLUMN_NAME, COLUMN_SCHEMA)
    def set_name(self, name: str):
        dict_set_value(self.__data, COLUMN_NAME, name, str)

    def get_alias(self) -> str:
        alias = dict_get_value(self.__data, COLUMN_ALIAS, COLUMN_SCHEMA)
        return alias if len(alias) > 0 else self.get_name()
    def set_alias(self, alias: str):
        dict_set_value(self.__data, COLUMN_ALIAS, alias, str)

    def get_type(self) -> Types:
        return dict_get_value(self.__data, COLUMN_TYPE, COLUMN_SCHEMA)
    def set_type(self, type: Types):
        dict_set_value(self.__data, COLUMN_TYPE, type, Types)

    def get_length(self) -> int:
        return dict_get_value(self.__data, COLUMN_LENGTH, COLUMN_SCHEMA)
    def set_length(self, length: int):
        dict_set_value(self.__data, COLUMN_LENGTH, length, int)

    def get_decimals(self) -> int:
        return dict_get_value(self.__data, COLUMN_DECIMALS, COLUMN_SCHEMA)
    def set_decimals(self, decimals: int):
        dict_set_value(self.__data, COLUMN_DECIMALS, decimals, int)

    def is_primary_key(self) -> bool:
        return dict_get_value(self.__data, COLUMN_PRIMARY_KEY, COLUMN_SCHEMA)
    def set_primary_key(self, primary_key: bool):
        dict_set_value(self.__data, COLUMN_PRIMARY_KEY, primary_key, int)

    def get_header(self) -> str:
        return dict_get_value(self.__data, COLUMN_HEADER, COLUMN_SCHEMA)
    def set_header(self, header: str):
        dict_set_value(self.__data, COLUMN_HEADER, header, int)

    def get_label(self) -> str:
        return dict_get_value(self.__data, COLUMN_LABEL, COLUMN_SCHEMA)
    def set_label(self, label: str):
        dict_set_value(self.__data, COLUMN_LABEL, label, int)

    def get_description(self) -> str:
        return dict_get_value(self.__data, COLUMN_DESCRIPTION, COLUMN_SCHEMA)
    def set_description(self, description: str):
        dict_set_value(self.__data, COLUMN_DESCRIPTION, description, int)

    def get_default_value(self) -> Value or None:
        type: Types = self.get_type()
        decs: int = self.get_decimals()
        decs = decs if decs >= 0 else 0
        if type is None: return None
        if type == Types.BOOLEAN: return Value(False)
        if type == Types.DECIMAL: return Value(round(Decimal(0), decs))
        if type == Types.INTEGER: return Value(int(0))
        if type == Types.FLOAT: return Value(float(0))
        if type == Types.COMPLEX: return Value(complex(0))
        if type == Types.DATE: return Value(Types.DATE)
        if type == Types.TIME: return Value(Types.TIME)
        if type == Types.DATETIME: return Value(Types.DATETIME)
        if type == Types.BINARY: return Value(bytes([]))
        if type == Types.STRING: return Value(str(""))
        if type == Types.LIST: return Value(list([]))
        if type == Types.DICTIONARY: return Value(dict({}))

    def get_table(self) -> Table:
        return dict_get_value(self.__data, COLUMN_TABLE, COLUMN_SCHEMA)
    def set_table(self, table: Table):
        dict_set_value(self.__data, COLUMN_TABLE, table, Table)

    def get_view(self) -> View:
        return dict_get_value(self.__data, COLUMN_VIEW, COLUMN_SCHEMA)
    def set_view(self, view: View):
        dict_set_value(self.__data, COLUMN_VIEW, view, View)

    def data(self) -> dict: return dict(self.__data)

    def __str__(self) -> str:
        return str(self.__data)
    def __repr__(self):
        return self.__str__()
