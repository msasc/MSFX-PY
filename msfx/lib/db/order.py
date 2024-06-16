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
from msfx.lib.util.error import check_argument_type

class Order:
    """ Order definition. """
    def __init__(self, order=None):
        self.__segments = []
        if order is not None:
            check_argument_type("order", order, (Order,))
            self.__segments.extend(order.__segments)

    def append(self, column, asc = True):
        check_argument_type("column", column, (Column,))
        check_argument_type("asc", asc, (bool,))
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
        check_argument_type("index", index, (int,))
        if 0 <= index < len(self):
            return self.__segments[index]
        return None
    def __str__(self) -> str:
        return str(self.to_dict())
    def __repr__(self):
        return self.__str__()
