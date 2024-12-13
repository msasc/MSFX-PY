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

from msfx.lib_back.db_back2.column import Column
from msfx.lib_back import error_msg

class Order:
    """ Order definition. """
    def __init__(self, order=None):
        self.__segments = []
        if order is not None:
            if not isinstance(order, Order):
                error = error_msg("type error", "order", type(order), (Order,))
                raise TypeError(error)
            self.__segments.extend(order.__segments)

    def append(self, column, asc = True):
        if column is None or not isinstance(column, Column):
            error = error_msg("type error", "column", type(column), (Column,))
            raise TypeError(error)
        if asc is None or not isinstance(asc, bool):
            error = error_msg("type error", "asc", type(asc), (bool,))
            raise TypeError(error)
        self.__segments.append({ "column": column, "asc": asc })

    def get_segments(self) -> list:
        return list(self.__segments)

    def to_dict(self):
        segments = []
        for segment in self.__segments:
            short_segment = {"column": segment["column"].get_name(), "asc": segment["asc"]}
            segments.append(short_segment)
        return {"segments": segments}

    def __iter__(self):
        return self.__segments.__iter__()
    def __len__(self) -> int:
        return len(self.__segments)
    def __getitem__(self, index) -> {}:
        if index is None or not isinstance(index, int):
            error = error_msg("type error", "index", type(index), (int,))
            raise TypeError(error)
        if 0 <= index < len(self):
            return self.__segments[index]
        return None
    def __str__(self) -> str:
        return str(self.to_dict())
    def __repr__(self):
        return self.__str__()
