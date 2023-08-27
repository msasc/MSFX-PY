#  Copyright (c) 2023 Miquel Sas.
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

from field import Field

class OrderSegment:
    """ An order segment definition. """
    def __init__(self, field: Field, asc: bool = True):
        """
        Creates a segment of an order or index.
        :param field: The field
        :param asc: The ascending flag.
        """
        # Validate arguments.
        if not isinstance(field, Field):
            raise Exception("Invalid type of argument 'field'")
        if not isinstance(asc, bool):
            raise Exception("Invalid type of argument 'asc'")
        # Member assignment.
        self.__field = Field(field)
        self.__asc = asc

    def get_field(self) -> Field:
        """
        Return the field.
        :return: The field.
        """
        return self.__field
    def is_asc(self) -> bool:
        """
        Return the ascending flag.
        :return: The ascending flag.
        """
        return self.__asc

    def __str__(self) -> str:
        """
        Return a string representation.
        :return: A string representation.
        """
        return f"{self.__field.get_name()}, {self.__asc}"

class Order:
    """ An order definition. """
    def __init__(self):
        self.__segments: list = []

    def append_segment(self, field: Field, asc: bool = True):
        """
        Add a segment.
        :param field: The field.
        :param asc: Optional ascending flag.
        """
        self.__segments.append(OrderSegment(field, asc))
    def get_segment(self, index: int) -> OrderSegment:
        """
        Return the segment at the given index.
        :param index: The index.
        """
        if not isinstance(index, int):
            raise Exception("Invalid type for argument 'index'")
        return self.__segments[index]

    def __iter__(self):
        """
        Iterator implementation.
        :return: The iterator.
        """
        return self.__segments.__iter__()
    def __len__(self) -> int:
        """
        Length implementation.
        :return: The length or number of segments.
        """
        return len(self.__segments)
    def __getitem__(self, index: int) -> OrderSegment:
        """
        Item access as a list.
        :param index: The index.
        :return: The segment.
        """
        if not isinstance(index, int):
            raise Exception("Invalid type for 'index' argument")
        return self.__segments[index]
    def __str__(self) -> str:
        """
        Return a string representation.
        :return: A string representation.
        """
        _str_: str = ""
        for i in range(len(self.__segments)):
            if i > 0:
                _str_ += ", "
            segment: OrderSegment = self.__segments[i]
            if isinstance(self, Index):
                _str_ += segment.get_field().get_name()
            else:
                _str_ += "["
                _str_ += str(self.__segments[i])
                _str_ += "]"
        return _str_
