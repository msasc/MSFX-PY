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

from msfx.lib.db.value import Value

class Field: pass
class Table: pass

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

class Index(Order):
    """ An index definition. """
    def __init__(self):
        super().__init__()
        self.__name: str or None = None
        self.__schema: str or None = None
        self.__unique: bool or None = None
        self.__table: Table = None

    def get_name(self) -> str or None:
        """
        Return the name.
        :return: The name.
        """
        return self.__name
    def get_schema(self) -> str or None:
        """
        Return the schema.
        :return: The index schema.
        """
        return self.__schema
    def is_unique(self) -> bool:
        """
        Check whether the index is unique.
        :return: A boolean.
        """
        if self.__unique is None: return False
        return self.__unique
    def get_table(self) -> Table:
        """
        Return the parent table.
        :return: The parent table.
        """
        return self.__table

    def set_name(self, name: str):
        """
        Set the name.
        :param name: The name.
        """
        if not isinstance(name, str):
            raise Exception("Invalid type for argument 'name'")
        self.__name = name
    def set_schema(self, schema: str):
        """
        Set the schema.
        :param schema: The schema.
        """
        if not isinstance(schema, str):
            raise Exception("Invalid type for argument 'schema'")
        self.__schema = schema
    def set_unique(self, unique: bool):
        """
        Set the unique flag.
        :param unique: A boolean.
        """
        if not isinstance(unique, bool):
            raise Exception("Invalid type for argument 'unique'")
        self.__unique = unique
    def set_table(self, table: Table):
        """
        Set the table.
        :param table: The table.
        """
        self.__table = table

    def __str__(self) -> str:
        _str_: str = self.get_name()
        if self.get_table() is not None:
            _str_ += " ON " + self.get_table().get_name()
        if self.is_unique(): _str_ += " UNIQUE"
        else: _str_ += " NOT UNIQUE"
        _str_ += " (" + super().__str__() + ")"
        return _str_

class OrderKeySegment:
    """ A segment of an order key, a pair made of a value and an ascending flag. """
    def __init__(self, value: Value, asc: bool = True):
        if not isinstance(value, Value):
            raise Exception("Invalid type for argument 'value'")
        self.__value = value
        self.__asc = asc

    def get_value(self) -> Value:
        """
        Returns the segment value.
        :return: The value.
        """
        return self.__value
    def is_asc(self) -> bool:
        """
        Returns the segment ascending flag.
        :return: A boolean.
        """
        return self.__asc

    def compare_to(self, other) -> int:
        if not isinstance(other, OrderKeySegment):
            raise TypeError(f"Not comparable argument {other}")
        compare: int = self.__value.compare_to(other.__value)
        mult: int = 1 if self.__asc else -1
        return compare * mult

    def __lt__(self, other) -> bool:
        return self.compare_to(other) < 0
    def __le__(self, other) -> bool:
        return self.compare_to(other) <= 0
    def __eq__(self, other) -> bool:
        return self.compare_to(other) == 0
    def __ne__(self, other) -> bool:
        return self.compare_to(other) != 0
    def __gt__(self, other) -> bool:
        return self.compare_to(other) > 0
    def __ge__(self, other) -> bool:
        return self.compare_to(other) >= 0

    def __str__(self) -> str:
        return "(" + str(self.__value) + ", " + str(self.__asc) + ")"


class OrderKey:
    """ An order key, a list of pairs [value, ascending flag]. """
    def __init__(self):
        self.__segments = []

    def append_segment(self, value: object, asc: bool = True):
        """
        Append a new segment.
        :param value: The value.
        :param asc: The ascending flag, defaults to true.
        """
        if not isinstance(value, Value):
            value = Value(value)
        self.__segments.append(OrderKeySegment(value, asc))

    def compare_to(self, other) -> int:
        """
        Compare this order key with another object.
        :param other: The other object.
        :return: A comparison integer.
        """
        if not isinstance(other, OrderKey):
            raise TypeError(f"Invalid type for argument {other}")
        len_min: int = min(len(self.__segments), len(other.__segments))
        for i in range(len_min):
            seg_self: OrderKeySegment = self.__segments[i]
            seg_comp: OrderKeySegment = other.__segments[i]
            compare = seg_self.compare_to(seg_comp)
            if compare != 0: return compare
        if len(self.__segments) < len(other.__segments): return -1
        if len(self.__segments) > len(other.__segments): return 1
        return 0

    def __len__(self) -> int:
        return len(self.__segments)

    def __lt__(self, other) -> bool:
        return self.compare_to(other) < 0
    def __le__(self, other) -> bool:
        return self.compare_to(other) <= 0
    def __eq__(self, other) -> bool:
        return self.compare_to(other) == 0
    def __ne__(self, other) -> bool:
        return self.compare_to(other) != 0
    def __gt__(self, other) -> bool:
        return self.compare_to(other) > 0
    def __ge__(self, other) -> bool:
        return self.compare_to(other) >= 0

    def __str__(self) -> str:
        string = "["
        for i in range(len(self.__segments)):
            if i > 0: string += ", "
            string += str(self.__segments[i])
        string += "]"
        return string
