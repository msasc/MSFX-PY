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

from msfx.lib import Data, merge_dicts, check_args
from msfx.lib.db.column import Column

class Order(Data):
    """ Order definition. """
    SEGMENTS = "segments"
    KEYS = [SEGMENTS]

    def __init__(self, order=None):
        self.__data = {"segments": []}
        if order is not None and isinstance(order, Order):
            self.from_dict(order.to_dict())

    def append(self, column: Column, asc: bool = True):
        check_args("type error", "column", column, (Column,))
        check_args("type error", "asc", type(asc), (bool,))
        self.__data[Order.SEGMENTS].append([column, asc])

    def get_column(self, index: int) -> Column: return self.__data[Order.SEGMENTS][index][0]
    def is_asc(self, index: int) -> bool: return self.__data[Order.SEGMENTS][index][1]

    def to_dict(self) -> dict: return dict(self.__data)
    def from_dict(self, data: dict): merge_dicts(data, self.__data, Order.KEYS)

    def __iter__(self): return self.__data[Order.SEGMENTS].__iter__()
    def __len__(self) -> int: return len(self.__data[Order.SEGMENTS])

    def __getitem__(self, index) -> {}:
        check_args("type error", "index", type(index), (int,))
        if 0 <= index < len(self): return self.__data[Order.SEGMENTS][index]
        return None
