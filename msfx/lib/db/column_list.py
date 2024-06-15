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

from typing import Optional

from msfx.lib.db.column import Column
from msfx.lib.db.schema import (
    COLUMNLIST_SCHEMA,
    COLUMNLIST_COLUMNS, COLUMNLIST_ALIASES, COLUMNLIST_INDEXES,
    COLUMNLIST_PK_COLUMNS, COLUMNLIST_DEFAULT_VALUES
)
from msfx.lib.util.generics import dict_get_value, dict_create_default
from msfx.lib.util.json import dumps

class ColumnList:
    """ An ordered list of columns that can be efficiently accessed either by index or alias. """
    def __init__(self):
        self.__data = dict_create_default(COLUMNLIST_SCHEMA)

    def append_column(self, column: Column, alias: Optional[str] = None):
        if column is None or not isinstance(column, Column):
            raise ValueError(f"column must be of type Column, not {type(column)}")
        column = Column(column)
        if alias is not None:
            column.set_alias(alias)
        self.get_columns().append(column)
        self.__setup()

    def remove_column(self, alias: str):
        index = self.get_indexes().get(alias)
        if index is not None:
            del self.get_columns()[index]
        self.__setup()

    def index_of_column(self, alias: str) -> int:
        index = self.get_indexes().get(alias)
        return -1 if index is None else index

    def get_column_by_alias(self, alias: str) -> Optional[Column]:
        index = self.index_of_column(alias)
        if index < 0:
            raise ValueError(f"Invalid alias {alias}")
        return self.get_columns()[index]

    def get_column_by_index(self, index: int) -> Optional[Column]:
        if not isinstance(index, int):
            raise ValueError(f"Index must be of type int, not {type(index)}")
        if index < 0:
            raise ValueError(f"Index must be >= 0, not {index}")
        if index >= len(self.get_columns()):
            raise ValueError(f"Index must be <= len(columns)")
        return self.get_columns()[index]

    def get_columns(self) -> list:
        return dict_get_value(self.__data, COLUMNLIST_COLUMNS, COLUMNLIST_SCHEMA)

    def get_pk_columns(self) -> list:
        return dict_get_value(self.__data, COLUMNLIST_PK_COLUMNS, COLUMNLIST_SCHEMA)

    def get_aliases(self) -> list:
        return dict_get_value(self.__data, COLUMNLIST_ALIASES, COLUMNLIST_SCHEMA)

    def get_default_values(self) -> list:
        return dict_get_value(self.__data, COLUMNLIST_DEFAULT_VALUES, COLUMNLIST_SCHEMA)

    def get_indexes(self) -> dict:
        return dict_get_value(self.__data, COLUMNLIST_INDEXES, COLUMNLIST_SCHEMA)

    def __setup(self):

        self.get_aliases().clear()
        self.get_indexes().clear()
        self.get_pk_columns().clear()
        self.get_default_values().clear()

        for i in range(len(self.get_columns())):
            column = self.get_columns()[i]
            alias = column.get_alias()
            self.get_aliases().append(alias)
            self.get_indexes()[alias] = i
            if column.is_primary_key():
                self.get_pk_columns().append(column)
            self.get_default_values().append(column.get_default_value())

    def __iter__(self):
        return self.get_columns().__iter__()
    def __len__(self) -> int:
        return len(self.get_columns())
    def __getitem__(self, index: int) -> Column:
        return self.get_column_by_index(index)
    def __str__(self) -> str:
        return str(self.__data)
    def __repr__(self):
        return self.__str__()
