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

from decimal import Decimal, ROUND_HALF_UP

from msfx.lib.db.types import Types, TYPES_LENGTH
from msfx.lib.db.value import Value
from msfx.lib.db.order import Order
from msfx.lib.db.json import JSON

class Table: pass

class Field:
    """
    Field metadata definition.
    """
    def __init__(self, field=None):
        """
        Default constructor.
        """
        self.__name: str or None = None
        self.__alias: str or None = None
        self.__type: Types or None = None
        self.__length: int or None = None
        self.__decimals: int or None = None

        self.__primary_key: bool = False
        self.__default_create_value: Value or None = None
        self.__table: Table or None = None
        self.__function: str or None = None

        self.__header: str or None = None
        self.__label: str or None = None
        self.__title: str or None = None

        self.__uppercase: bool = True
        self.__display_length: int or None = None
        self.__display_decimals: int or None = None

        self.__properties: dict = {}

        if field is not None:
            if not isinstance(field, Field):
                raise Exception("Argument field must be a Field instance")

            self.__name = field.__name
            self.__alias = field.__alias
            self.__type = field.__type
            self.__length = field.__length
            self.__decimals = field.__decimals

            self.__primary_key = field.__primary_key

            self.__default_create_value = field.__default_create_value
            self.__table = field.__table
            self.__function = field.__function

            self.__header = field.__header
            self.__label = field.__label
            self.__title = field.__title

            self.__uppercase = field.__uppercase
            self.__display_length = field.__display_length
            self.__display_decimals = field.__display_decimals

            self.__properties |= field.__properties

    def get_name(self) -> str or None:
        """
        Returns the name of the field.
        :return: The name.
        """
        return self.__name
    def get_alias(self) -> str or None:
        """
        Returns the alias of the field.
        :return: The alias.
        """
        if self.__alias is None:
            return self.get_name()
        return self.__alias
    def get_type(self) -> Types or None:
        """
        Returns the type of the field.
        :return: The type.
        """
        return self.__type
    def get_length(self) -> int or None:
        """
        Returns the length of the field if applies.
        :return: The length.
        """
        return self.__length
    def get_decimals(self) -> int or None:
        """
        Returns the number f decimal places of the field if applies.
        :return: The decimals.
        """
        return self.__decimals

    def set_name(self, name: str):
        """
        Set the name.
        :param name: The field name.
        """
        if not isinstance(name, str): raise Exception("Invalid argument type")
        self.__name = name
    def set_alias(self, alias: str):
        """
        Set the alias.
        :param alias: The alias.
        """
        if not isinstance(alias, str): raise Exception("Invalid argument type")
        self.__alias = alias
    def set_type(self, type: Types):
        """
        Set the type.
        :param type:  The type.
        """
        if not isinstance(type, Types): raise Exception("Invalid argument type")
        self.__type = type
    def set_length(self, length: int):
        """
        Set the length.
        :param length:  The length.
        """
        if not isinstance(length, int): raise Exception("Invalid argument type")
        if length <= 0: raise Exception("Invalid argument value")
        if self.__type not in TYPES_LENGTH:
            raise Exception(f"Only types {TYPES_LENGTH} admits the 'length' property.")
        self.__length = length
    def set_decimals(self, decimals: int):
        """
        Set the number of decimal places.
        :param decimals: The decimals.
        """
        if not isinstance(decimals, int): raise Exception("Invalid argument type")
        if decimals < 0: raise Exception("Invalid argument value")
        if self.__type is not Types.DECIMAL: raise Exception("Field type is not DECIMAL")
        self.__decimals = decimals

    def get_default_create_value(self):
        """
        Returns the default create value.
        :return: The default create value.
        """
        return self.__default_create_value
    def get_default_value(self) -> Value:
        """
        Returns the default.
        :return: The default value.
        """
        if self.__type == Types.BOOLEAN: return Value(False)
        if self.__type == Types.DECIMAL:
            decimals = self.__decimals
            if decimals is None: decimals = 0
            return Value(Decimal(0).quantize(Decimal(10) ** -decimals, rounding=ROUND_HALF_UP))
        if self.__type == Types.INTEGER: return Value(int(0))
        if self.__type == Types.FLOAT: return Value(float(0))
        if self.__type == Types.COMPLEX: return Value(complex(0))
        if self.__type == Types.DATE: return Value(Types.DATE)
        if self.__type == Types.TIME: return Value(Types.TIME)
        if self.__type == Types.DATETIME: return Value(Types.DATETIME)
        if self.__type == Types.BINARY: return Value(bytes([]))
        if self.__type == Types.STRING: return Value("")
        if self.__type == Types.JSON: return Value(JSON())
        raise Exception("Never should have come here!!")

    def set_default_create_value(self, value: Value):
        """
        Set the default create value.
        :param value: The value.
        """
        if not isinstance(value, Value): raise Exception("Invalid argument type")
        self.__default_create_value = value

    def is_primary_key(self) -> bool:
        """
        Check whether the field is a primary key field.
        :return: A boolean.
        """
        return self.__primary_key
    def is_persistent(self) -> bool:
        """
        Check whether this field is persistent. A field is persistent if it is not a function
        and belongs to a table.
        :return: A boolean.
        """
        if self.is_virtual(): return False
        return self.__table is not None
    def is_nullable(self) -> bool:
        """
        Check whether the field is nullable.
        :return: A boolean.
        """
        if self.is_primary_key(): return False
        if self.is_boolean() or self.is_numeric(): return False
        return True

    def set_primary_key(self, primary_key: bool):
        """
        Set whether this field is a primary key field.
        :param primary_key: A boolean.
        """
        if not isinstance(primary_key, bool): raise Exception("Invalid argument type")
        self.__primary_key = primary_key

    def get_table(self) -> Table:
        """
        Return this field parent table if any.
        :return: The parent table.
        """
        return self.__table
    def set_table(self, table: Table):
        """
        Set the parent table.
        :param table: The parent table.
        """
        if not isinstance(table, Table): raise Exception("Invalid argument type")
        self.__table = table

    def get_function(self) -> str or None:
        """
        Return the function.
        :return: The database function.
        """
        return self.__function
    def set_function(self, function: str or None):
        """
        Set the function.
        :param function: The function.
        """
        if function is None:
            self.__function = None
            return
        if not isinstance(function, str): raise Exception("Invalid argument type")
        if len(function) == 0: raise Exception("Invalid empty function")
        self.__function = function
        self.__table = None

    def is_virtual(self) -> bool:
        """
        Check whether this field is virtual, that is, is a function.
        :return: A boolean.
        """
        return self.__function is not None and len(self.__function) > 0

    def get_name_group_by(self):
        """
        Return the name to use in a GROUP BY clause.
        :return: The name.
        """
        return self.get_name_select()
    def get_name_order_by(self):
        """
        Return the name to use in an ORDER BY clause.
        :return: The name.
        """
        return self.get_name_select()
    def get_name_parent(self) -> str:
        """
        Returns the name qualified with the parent table alias if present.
        :return: The name qualified with the parent table alias if present.
        """
        if self.get_table() is not None:
            return self.get_table().get_alias() + "." + self.get_name()
        return self.get_name()
    def get_name_select(self) -> str:
        """
        Returns the name to use in a SELECT clause of a select query.
        :return: The name to use in a SELECT clause.
        """
        if self.is_virtual():
            return "(" + self.get_function() + ")"
        return self.get_name_parent()

    def get_header(self):
        """
        Return the header in a table view.
        :return: The header.
        """
        return self.__header
    def get_label(self):
        """
        Return the label in a form view.
        :return: The label.
        """
        return self.__label
    def get_title(self):
        """
        Return the title or description.
        :return: The title.
        """
        return self.__title

    def set_header(self, header: str):
        """
        Set the header in table views.
        :param header: The header.
        """
        self.__header = header
    def set_label(self, label: str):
        """
        Set the label in table views.
        :param label: The label.
        """
        self.__label = label
    def set_title(self, title: str):
        """
        Set the title or description.
        :param title: The title.
        """
        self.__title = title

    def is_uppercase(self):
        """
        Check whether this field is uppercase.
        :return: A boolean.
        """
        return self.__uppercase
    def set_uppercase(self, uppercase: bool):
        """
        Set whether this field value should be uppercase.
        :param uppercase: A boolean.
        """
        self.__uppercase = uppercase

    def get_display_length(self):
        """
        Return the display length.
        :return: The display length.
        """
        if self.__display_length is None or self.__display_length <= 0:
            return self.get_length()
        return self.__display_length
    def get_display_decimals(self):
        """
        Return the display decimals.
        :return: The display decimals.
        """
        if self.__display_decimals is None or self.__display_decimals <= 0:
            return self.get_decimals()
        return self.__display_decimals

    def set_display_length(self, length: int or None):
        """
        Set the display length.
        :param length: The display length.
        """
        self.__display_length = length
    def set_display_decimals(self, decimals: int or None):
        """
        Set the display decimals.
        :param decimals: The display decimals.
        """
        self.__display_decimals = decimals

    def get_properties(self) -> dict: return self.__properties

    def is_boolean(self) -> bool:
        """
        Check whether the value is boolean.
        :return: A bool.
        """
        return self.__type == Types.BOOLEAN
    def is_decimal(self) -> bool:
        """
        Check whether the value is a decimal.
        :return: A bool.
        """
        return self.__type == Types.DECIMAL
    def is_integer(self) -> bool:
        """
        Check whether the value is an integer.
        :return: A bool.
        """
        return self.__type == Types.INTEGER
    def is_float(self) -> bool:
        """
        Check whether the value is a float.
        :return: A bool.
        """
        return self.__type == Types.FLOAT
    def is_complex(self) -> bool:
        """
        Check whether the value is a complex.
        :return: A bool.
        """
        return self.__type == Types.COMPLEX
    def is_string(self) -> bool:
        """
        Check whether the value is a string.
        :return: A bool.
        """
        return self.__type == Types.STRING
    def is_date(self) -> bool:
        """
        Check whether the value is a date. A date value can be None.
        :return: A bool.
        """
        return self.__type == Types.DATE
    def is_time(self) -> bool:
        """
        Check whether the value is a time. A time value can be None.
        :return: A bool.
        """
        return self.__type == Types.TIME
    def is_datetime(self) -> bool:
        """
        Check whether the value is a date-time. A date-time value can be None.
        :return: A bool.
        """
        return self.__type == Types.DATETIME
    def is_binary(self) -> bool:
        """
        Check whether the value is a binary value. A binary value can be None.
        :return: A bool.
        """
        return self.__type == Types.BINARY
    def is_JSON(self) -> bool:
        """
        Check whether this value is a JSON object.
        :return: A boolean.
        """
        return self.__type == Types.JSON

    def is_numeric(self) -> bool:
        """
        Check whether the value is a numeric value.
        :return: A bool.
        """
        numeric: bool = (
            self.__type == Types.DECIMAL or
            self.__type == Types.INTEGER or
            self.__type == Types.FLOAT or
            self.__type == Types.COMPLEX
        )
        return numeric

    def __eq__(self, other: object) -> bool:
        """
        Check for equality.
        :param other: The object to check.
        :return: A boolean.
        """
        if not isinstance(other, Field): return False
        equals: bool = True
        if equals: equals = equals and self.get_name() == other.get_name()
        if equals: equals = equals and self.get_alias() == other.get_alias()
        if equals: equals = equals and self.get_type() == other.get_type()
        if equals: equals = equals and self.get_length() == other.get_length()
        if equals: equals = equals and self.get_decimals() == other.get_decimals()
        if equals: equals = equals and self.get_table() == other.get_table()
        return equals
    def __str__(self) -> str:
        """
        Returns a string representation of this field.
        :return: A string representation.
        """
        s: str = str(self.get_name()) + ", " + str(self.get_type())
        if self.__length is not None: s += ", " + str(self.get_length())
        if self.__decimals is not None: s += ", " + str(self.get_decimals())
        if self.__table is not None: s += ", " + str(self.get_table())
        if len(self.__properties) > 0: s += f", props ({self.__properties})"
        return s
    def __hash__(self):
        """
        Return the hash code.
        :return: The hash code.
        """
        return hash(self.get_name_parent())


class FieldList:
    """
    An ordered list of fields that can efficiently be accessed by index or by alias.
    The aliases must be unique. Appending a field with the alias of an existing one raises an error.
    """
    def __init__(self):
        self.__fields: list = []
        self.__aliases: list = []
        self.__indexes: dict = {}
        self.__persistent_fields: list = []
        self.__primary_key_fields: list = []
        self.__primary_key_indexes: list = []
        self.__default_values: list = []

    def append_field(self, field: Field) -> None:
        """
        Append a new field.
        :param field: The field to append to the list.
        """
        if not isinstance(field, Field):
            raise Exception("Invalid type for argument 'field'")
        self.__fields.append(Field(field))
        self.__setup__()
    def get_field(self, key: int or str) -> Field:
        """
        Returns the field or None.
        :param key: The key, the alias or the index.
        :return: The field if found.
        """
        if not (isinstance(key, int) or not isinstance(key, str)):
            raise Exception(f"Invalid argument type for 'key': {type(key)}")
        if isinstance(key, int): return self.__fields[key]
        return self.__fields[self.index_of(key)]
    def get_persistent_fields(self) -> tuple:
        """
        Returns the list of persistent fields.
        :return: The list of persistent fields.
        """
        return tuple(self.__persistent_fields)
    def get_primary_key_fields(self) -> tuple:
        """
        Returns the list of primary key fields.
        :return: The list of primary key fields.
        """
        return tuple(self.__primary_key_fields)
    def get_primary_key_indexes(self) -> tuple:
        """
        Returns the list of primary key indexes.
        :return: The list of primary key indexes.
        """
        return tuple(self.__primary_key_indexes)
    def get_primary_order(self) -> Order:
        """
        Return the primary order.
        :return: The primary order.
        """
        order: Order = Order()
        for field in self.__primary_key_fields:
            order.append_segment(field)
        return order

    def index_of(self, alias: str) -> int:
        """
        Returns the index of a field given the alias.
        :param alias: The field alias.
        :return: The index in the list of fields.
        """
        if not isinstance(alias, str):
            raise Exception("Invalid type for argument key")
        index: int or None = self.__indexes.get(alias)
        if index is None:
            raise Exception(f"Invalid key or alias: {alias}")
        return index

    def fields(self) -> tuple:
        """
        Returns the list of fields as an unmodifiable tuple.
        :return: The list of fields.
        """
        return tuple(self.__fields)
    def aliases(self) -> tuple:
        """
        Returns the list of aliases as an unmodifiable tuple.
        :return: The list of aliases.
        """
        return tuple(self.__aliases)

    def __setup__(self) -> None:
        """
        Setup internal lists and maps based on the current list of fields.
        """

        self.__aliases.clear()
        self.__indexes.clear()
        self.__persistent_fields.clear()
        self.__primary_key_fields.clear()
        self.__primary_key_indexes.clear()
        self.__default_values.clear()

        for i in range(len(self.__fields)):
            field: Field = self.__fields[i]
            alias: str = field.get_alias()
            self.__aliases.append(alias)
            self.__indexes[alias] = i
            if field.is_persistent():
                self.__persistent_fields.append(field)
            if field.is_primary_key():
                self.__primary_key_fields.append(field)
                self.__primary_key_indexes.append(i)
            self.__default_values.append(field.get_default_value())

    def __iter__(self):
        """
        Iterator implementation on fields.
        :return: The iterator on fields.
        """
        return self.__fields.__iter__()
    def __len__(self) -> int:
        """
        Length implementation.
        :return: The length or number of fields.
        """
        return len(self.__fields)
    def __getitem__(self, index: int) -> Field:
        """
        Field accesses as a list.
        :param index: The index.
        :return: The field.
        """
        if not isinstance(index, int):
            raise Exception("Invalid type for 'index' argument")
        return self.__fields[index]
