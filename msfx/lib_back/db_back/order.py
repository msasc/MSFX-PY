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
from msfx.lib_back.db_back.column import Column
from msfx.lib_back.dn import Schema, create_from_schema, get_list, dumps, loads, register_class
from msfx.lib_back import error_msg

class Order:
    """ Order definition. """

    SEGMENTS = "segments"

    schema = Schema()
    schema.add(key=SEGMENTS, value_type=list, default_value=[])

    def __init__(self, order=None):
        self.__data = create_from_schema(Order.schema)
        if order is not None and isinstance(order, Order):
            self.__data |= order.__data
        if order is not None and isinstance(order, dict):
            self.__data |= order

    def _data(self): return self.__data
    def __segments(self): return get_list(self.__data, Order.SEGMENTS)

    def get_column(self, index: int) -> Column: return self.__segments()[index][0]
    def is_asc(self, index: int) -> bool: return self.__segments()[index][1]

    def append(self, column: Column, asc: bool = True):
        if column is None or not isinstance(column, Column):
            error = error_msg("type error", "column", type(column), (Column,))
            raise TypeError(error)
        if asc is None or not isinstance(asc, bool):
            error = error_msg("type error", "asc", type(asc), (bool,))
            raise TypeError(error)
        self.__segments().append([column, asc])

    def to_string(self, **kwargs) -> str: return dumps(self.__data, **kwargs)
    def from_string(self, data: str): self.__data = loads(data)
    def to_dict(self) -> dict: return dict(self.__data)

    def __iter__(self): return self.__segments().__iter__()
    def __len__(self) -> int: return len(self.__segments())

    def __getitem__(self, index) -> {}:
        if index is None or not isinstance(index, int):
            error = error_msg("type error", "index", type(index), (int,))
            raise TypeError(error)
        if 0 <= index < len(self):
            return self.__segments()[index]
        return None

    def __str__(self) -> str: return str(self.__data)
    def __repr__(self): return self.__str__()

register_class("order", Order)
