#  Copyright (c) 2025 Miquel Sas.
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

from typing import Optional, Tuple

from msfx.lib.db import Value
from msfx.lib.db.md import ColumnList, Column

class Record:
    def __init__(self, columns: ColumnList, values: Tuple[Value, ...]):
        if not isinstance(columns, ColumnList): raise TypeError("Invalid columns")
        if not isinstance(values, tuple): raise TypeError("Invalid values")
        if len(columns) != len(values): raise ValueError("Invalid columns/values")
        self.__columns: ColumnList = columns
        self.__values: Tuple[Value, ...] = values

    @property
    def columns(self) -> ColumnList: return self.__columns
    @property
    def values(self) -> Tuple[Value, ...]: return self.__values

    def size(self): return len(self.__values)

    def get_column_by_alias(self, alias: str) -> Column:
        return self.__columns.get_by_alias(alias)
    def get_column_by_index(self, index: int) -> Column:
        return self.__columns.get_by_index(index)

    def get_value_by_alias(self, alias: str) -> Value:
        index = self.__columns.index_of(alias)
        return self.__values[index]
    def get_value_by_index(self, index: int) -> Value:
        return self.__values[index]

    def __str__(self) -> str: return str(self.__values)
    def __repr__(self): return self.__str__()
