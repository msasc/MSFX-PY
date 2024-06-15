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
from msfx.lib.db.column import Column
from msfx.lib.util.generics import dict_create_default, dict_get_value
from msfx.lib.db.schema import ORDER_SCHEMA, ORDER_SEGMENTS, ORDER_COLUMN, ORDER_ASC

class Order:
    """ Order definition. """
    def __init__(self, order=None):
        self.__data = dict_create_default(ORDER_SCHEMA)

    def append(self, column: Column, asc: bool = True):
        if not isinstance(column, Column):
            raise ValueError("Column must be of type Column")
        segment = {ORDER_COLUMN: column, ORDER_ASC: asc}
        self.get_segments().append(segment)

    def get_segments(self) -> list:
        return dict_get_value(self.__data, ORDER_SEGMENTS, ORDER_SCHEMA)

    def __iter__(self):
        return self.get_segments().__iter__()
    def __len__(self) -> int:
        return len(self.get_segments())
    def __getitem__(self, index: int) -> {}:
        if not isinstance(index, int):
            raise ValueError("Index must be of type int")
        if 0 <= index < len(self):
            return self.get_segments()[index]
        return None
    def __str__(self) -> str:
        s = "'" + ORDER_SEGMENTS + "': ["
        segs = self.get_segments()
        for i in range(len(segs)):
            seg = segs[i]
            if i > 0: s += ", "
            s += "{'" + ORDER_COLUMN + "': '" + seg[ORDER_COLUMN].get_name() + "'"
            s += ", '" + ORDER_ASC + "': " + str(seg[ORDER_ASC])
            s += "}"
        s += "]"
        return s
    def __repr__(self):
        return self.__str__()
