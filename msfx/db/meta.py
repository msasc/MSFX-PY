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
"""
The meta module packs the metadata definitions.
"""

import json
from enum import Enum, EnumMeta
from decimal import Decimal, ROUND_HALF_UP
from datetime import date, time, datetime

# Forward class declarations to avoid circularities
class Table: pass
class View: pass

class Types(Enum, metaclass=EnumMeta):
    """	Supported types mapped to the underlying SQL databases. """
    BOOLEAN = 0
    """
    A boolean value that is supported in the database either by a BIT
    type or a Y/N or T/F single byte string.
    """
    DECIMAL = 10
    """ A numeric value with fixed number of decimal places. """
    INTEGER = 11
    """ A numeric integer or long value. """
    FLOAT = 13
    """ A numeric double (float) value. """
    COMPLEX = 14
    """ A numeric complex value. """
    DATE = 20
    """ A date value with ISO format '2022-12-21' """
    TIME = 21
    """ A time value with ISO format '10:25:05.135000000' """
    DATETIME = 22
    """ A date-time value with ISO format '2022-12-21T10:25:05.135000000' """
    BINARY = 30
    """
    A binary value, stored in the underlying database in fields of types
    for instance TINYBLOB, BLOB, MEDIUMBLOB or LONGBLOB depending on the length.
    """
    STRING = 40
    """
    A string value, stored in the underlying database in fields of types
    for instance VARCHAR, TINYTEXT, TEXT, MEDIUMTEXT or LONGTEXT depending on the length. 
    """
    JSON = 50
    """
    A JSON object value, stored in the underlying database as a STRING.
    """

class JSON:
    """ JSON value encapsulation. """
    def __init__(self) -> None:
        """ Creates an empty JSON object."""
        self.__data: dict = {}
    def __init(self, json_data) -> None:
        """ Creates a JSON object dumping json string data. """
        self.__data: dict = json.loads(json_data)
    def loads(self, json_data) -> None:
        """ Loads the argument json_data string and merges it with this JSON internal dictionary data. """
        self.__data |= json.loads(json_data)
    def dumps(self) -> str:
        """ Dumps the internal dictionary data and returns a json string representation. """
        return json.dumps(self.__data)
    def merge(self, data: dict) -> None:
        """ Merges the argument dictionary data with this JSON internal dictionary data. """
        if type(data) is not dict: raise "Data to merge must be of dict type"
        self.__data |= data
    def data(self) -> dict:
        """ Gives access to the internal Python data dictionary. """
        return self.__data

    def __str__(self) -> str: return str(self.__data)
    def __eq__(self, other: object) -> bool:
        if isinstance(other, JSON): return self.__data == other.__data
        if isinstance(other, dict): return self.__data == other
        return super().__eq__(other)

class Value:
    """
    A value encapsulates a reference to one of the supported types. Except for the JSON type,
    which internally is a dictionary, the rest of value type can be considered immutable.
    """
    def __init__(self, value):
        """
        Constructs a Value with one of the supported types.
        :param value: The data value or the Types type and the internal value will be None.
        """

        # Argument value can not be None.
        if value is None:
            raise Exception("Argument value can not be None.")

        self.__value = None
        self.__type = None

        # The type is passed as argument value is None, and we are done.
        if isinstance(value, Types): self.__type = value; return

        # Assing the proper type or raise an exception if not supported.
        if isinstance(value, bool): self.__type = Types.BOOLEAN
        elif isinstance(value, Decimal): self.__type = Types.DECIMAL
        elif isinstance(value, int): self.__type = Types.INTEGER
        elif isinstance(value, float): self.__type = Types.FLOAT
        elif isinstance(value, complex): self.__type = Types.COMPLEX
        elif isinstance(value, date): self.__type = Types.DATE
        elif isinstance(value, time): self.__type = Types.TIME
        elif isinstance(value, datetime): self.__type = Types.DATETIME
        elif isinstance(value, bytes): self.__type = Types.BINARY
        elif isinstance(value, str): self.__type = Types.STRING
        elif isinstance(value, JSON): self.__type = Types.JSON
        else: raise Exception(f"Invalid type for argument value: {type(value)}")

        # Assign the value.
        self.__value = value

    def type(self) -> Types: return self.__type
    def value(self) -> object: return self.__value

    def is_none(self) -> bool: return self.__value is None
    def is_boolean(self) -> bool: return self.__type == Types.BOOLEAN
    def is_decimal(self) -> bool: return self.__type == Types.DECIMAL
    def is_integer(self) -> bool: return self.__type == Types.INTEGER
    def is_float(self) -> bool: return self.__type == Types.FLOAT
    def is_complex(self) -> bool: return self.__type == Types.COMPLEX
    def is_date(self) -> bool: return self.__type == Types.DATE
    def is_time(self) -> bool: return self.__type == Types.TIME
    def is_datetime(self) -> bool: return self.__type == Types.DATETIME
    def is_binary(self) -> bool: return self.__type == Types.BINARY
    def is_string(self) -> bool: return self.__type == Types.STRING
    def is_JSON(self) -> bool: return self.__type == Types.JSON

    def is_numeric(self) -> bool:
        if (self.__type == Types.DECIMAL or
            self.__type == Types.INTEGER or
            self.__type == Types.FLOAT or
            self.__type == Types.COMPLEX):
            return True
        return False

    def get_boolean(self) -> bool:
        if not self.is_boolean(): raise Exception("Type is not BOOLEAN")
        if self.is_none(): return False
        return bool(self.__value)

    def get_decimal(self) -> Decimal:
        if not self.is_numeric(): raise Exception("Type is not NUMERIC")
        if self.is_none(): return Decimal(0)
        return Decimal(self.__value)

    def get_integer(self) -> int:
        if not self.is_numeric(): raise Exception("Type is not NUMERIC")
        if self.is_none(): return 0
        return int(self.__value)

    def get_float(self) -> float:
        if not self.is_numeric(): raise Exception("Type is not NUMERIC")
        if self.is_none(): return 0.0
        return float(self.__value)

    def get_complex(self) -> complex:
        if not self.is_numeric(): raise Exception("Type is not NUMERIC")
        if self.is_none(): return complex(0)
        return complex(self.__value)

    def get_date(self) -> date or None:
        if not self.is_date(): raise Exception("Type is not DATE.")
        if self.is_none(): return None
        return self.__value

    def get_time(self) -> time or None:
        if not self.is_time(): raise Exception("Type is not TIME.")
        if self.is_none(): return None
        return self.__value

    def get_datetime(self) -> datetime or None:
        if not self.is_datetime(): raise Exception("Type is not DATETIME.")
        if self.is_none(): return None
        return self.__value

    def get_binary(self) -> bytes:
        if not self.is_binary(): raise Exception("Type is not BINARY.")
        if self.is_none(): return bytes([])
        return self.__value

    def get_string(self) -> str:
        if not self.is_string(): raise Exception("Type is not STRING.")
        if self.is_none(): return ""
        return self.__value

    def get_JSON(self) -> JSON:
        if not self.is_JSON(): raise Exception("Type is not JSON.")
        if self.is_none(): return JSON()
        return self.__value

    def __lt__(self, other: object) -> bool: return super().__lt__(other)
    def __le__(self, other: object) -> bool: return super().__le__(other)

    def __eq__(self, other: object) -> bool:
        # Other is a Value.
        if isinstance(other, Value): return self.__value == other.__value
        # Other is comparable.
        comparable: bool = False
        if self.is_boolean(): comparable = isinstance(other, bool)
        if self.is_numeric():
            comparable = (
                isinstance(other, Decimal) or
                isinstance(other, int) or
                isinstance(other, float) or
                isinstance(other, complex)
            )
        if self.is_date(): comparable = isinstance(other, date)
        if self.is_time(): comparable = isinstance(other, time)
        if self.is_datetime(): comparable = isinstance(other, datetime)
        if self.is_binary(): comparable = isinstance(other, bytes)
        if self.is_string(): comparable = isinstance(other, str)
        if self.is_JSON(): comparable = isinstance(other, JSON)
        if comparable: return self.__value == other
        return False

    def __ne__(self, other: object) -> bool: return super().__ne__(other)
    def __gt__(self, other: object) -> bool: return super().__gt__(other)
    def __ge__(self, other: object) -> bool: return super().__ge__(other)

    def __str__(self) -> str:
        if self.is_none(): return ""
        return str(self.__value)

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

        self.__persistent: bool = False
        self.__primary_key: bool = False
        self.__nullable: bool = True

        self.__function: str or None = None

        self.__table: Table or None = None
        self.__view: View or None = None

        self.__properties: dict = {}

        if field is not None:
            if not isinstance(field, Field): raise Exception("Argument field must be a Field instance")
            self.__name = field.__name
            self.__alias = field.__alias
            self.__type = field.__type
            self.__length = field.__length
            self.__decimals = field.__decimals

            self.__persistent = field.__persistent
            self.__primary_key = field.__primary_key
            self.__nullable = field.__nullable

            self.__function = field.__function

            self.__table = field.__table
            self.__view = field.__view

            self.__properties |= field.__properties

    def get_name(self) -> str or None: return self.__name
    def get_alias(self) -> str or None:
        if self.__alias is None: return self.get_name()
        return self.__alias
    def get_type(self) -> Types or None: return self.__type
    def get_length(self) -> int or None: return self.__length
    def get_decimals(self) -> int or None: return self.__decimals

    def is_persistent(self) -> bool:
        if self.__function is not None and len(self.__function) > 0: return False
        return self.__persistent
    def is_primary_key(self) -> bool: return self.__primary_key
    def is_nullable(self) -> bool: return self.__nullable

    def is_virtual(self) -> bool: return self.__function is not None
    def get_function(self) -> str or None: return self.__function

    def get_table(self) -> Table or None: return self.__table
    def get_view(self) -> View or None: return self.__view

    def get_properties(self) -> dict: return self.__properties

    def get_default_value(self) -> Value:
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

    def set_name(self, name: str):
        if not isinstance(name, str): raise Exception("Invalid argument type")
        self.__name = name
    def set_alias(self, alias: str):
        if not isinstance(alias, str): raise Exception("Invalid argument type")
        self.__alias = alias
    def set_type(self, type: Types):
        if not isinstance(type, Types): raise Exception("Invalid argument type")
        self.__type = type
    def set_length(self, length: int):
        if not isinstance(length, int): raise Exception("Invalid argument type")
        if length <= 0: raise Exception("Invalid argument value")
        types_length = [
            Types.DECIMAL,
            Types.STRING,
            Types.BINARY
        ]
        if self.__type not in types_length:
            raise Exception(f"Only types {types_length} admits the 'length' property.")
        self.__length = length
    def set_decimals(self, decimals: int):
        if not isinstance(decimals, int): raise Exception("Invalid argument type")
        if decimals < 0: raise Exception("Invalid argument value")
        if self.__type is not Types.DECIMAL: raise Exception("Field type is not DECIMAL")
        self.__decimals = decimals

    def set_persistent(self, persistent: bool):
        if not isinstance(persistent, bool): raise Exception("Invalid argument type")
        self.__persistent = persistent
    def set_primary_key(self, primary_key: bool):
        if not isinstance(primary_key, bool): raise Exception("Invalid argument type")
        self.__primary_key = primary_key
    def set_nullable(self, nullable: bool):
        if not isinstance(nullable, bool): raise Exception("Invalid argument type")
        self.__nullable = nullable

    def set_function(self, function: str or None):
        if function is None:
            self.__function = None
            return
        if not isinstance(function, str): raise Exception("Invalid argument type")
        if len(function) == 0: raise Exception("Invalid empty function")
        self.__function = function

    def set_table(self, table: Table or None):
        if table is not None and not isinstance(table, Table): raise Exception("Invalid argument type")
        self.__table = table
    def set_view(self, view: View or None):
        if view is not None and not isinstance(view, View): raise Exception("Invalid argument type")
        self.__view = view

    def __eq__(self, other: object) -> bool:
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
        s: str = str(self.get_name()) + ", " + str(self.get_type())
        if self.__length is not None: s += ", " + str(self.get_length())
        if self.__decimals is not None: s += ", " + str(self.get_decimals())
        if self.__table is not None: s += ", table: " + str(self.get_table().get_name())
        return s

class Fields:
    """
    An ordered list of fields that can efficiently be accessed by index or by key or field alias.
    The aliases must be unique. Appending a field with the alias of an existing one raises an error.
    """
    def __init__(self):
        self.__fields: list = []
        self.__keys: list = []
        self.__indexes: dict = {}

        self.__persistent_fields: list = []
        self.__primary_key_fields: list = []
        self.__default_values: list = []

    def append_field(self, field: Field) -> None:
        """
        Append a new field.
        :param field: The field to append to the list.
        """
        if not isinstance(field, Field): raise Exception("Invalid type for argument 'field'")
        self.__fields.append(Field(field))
        self.__setup__()

    def get_field(self, key: int or str) -> Field:
        if not (isinstance(key, int) or isinstance(key, str)):
            raise Exception(f"Invalid argument type for 'key': {type(key)}")
        if isinstance(key, int): return self.__fields[key]
        return self.__fields[self.index_of(key)]

    def get_persistent_fields(self) -> list: return list(self.__persistent_fields)
    def get_primary_key_fields(self) -> list: return list(self.__primary_key_fields)
    def get_default_values(self) -> list: return list(self.__default_values)

    def index_of(self, key: str) -> int:
        if not isinstance(key, str): raise Exception("Invalid type for argument key")
        index: int or None = self.__indexes.get(key)
        if index is None: raise Exception(f"Invalid key or alias: {key}")
        return index

    def fields(self) -> list: return list(self.__fields)
    def keys(self) -> list: return list(self.__keys)

    def contains(self, field: Field) -> bool:
        for fld in self.__fields:
            if fld == field: return True
        return False

    def __setup__(self) -> None:
        """
        Setup internal lists and maps based on the current list of fields.
        """
        self.__keys.clear()
        self.__indexes.clear()
        self.__persistent_fields.clear()
        self.__primary_key_fields.clear()
        self.__default_values.clear()

        for i in range(len(self.__fields)):
            field: Field = self.__fields[i]
            key: str = field.get_alias()
            self.__keys.append(key)
            self.__indexes[key] = i
            if field.is_persistent(): self.__persistent_fields.append(field)
            if field.is_primary_key(): self.__primary_key_fields.append(field)
            self.__default_values.append(field.get_default_value())

    def __iter__(self):
        """
        Implementation of the iterator functionallity using the fields list iterator.
        :return: An iterator through the list of fields.
        """
        return self.__fields.__iter__()

    def __len__(self): return len(self.__fields)
    def __getitem__(self, index: int) -> Field:
        if not isinstance(index, int): raise Exception("Invalid type for 'index' argument")
        return self.__fields[index]

class Record:
    """ A record packs a list of values and their corresponding field definitions. """
    def __init__(self, fields: Fields, values: list or None = None):
        if not isinstance(fields, Fields):
            raise Exception("Invalid type for argument 'fields'")
        if values is not None and not isinstance(values, list):
            raise Exception("Invalid type for argument 'values'")
        self.__fields = fields
        self.__values: list or None = None
        if isinstance(values, list):
            self.__values = values
        else:
            self.__values = fields.get_default_values()
        pass

class OrderSegment:
    """ An order segment definition. """
    def __init__(self, field: Field, asc: bool = True):
        """
        Creates a segment of an order or index.
        :param field: The field
        :param asc: The ascending flag.
        """
        # Validate arguments.
        if not isinstance(field, Field): raise Exception("Invalid type of argument 'field'")
        if not isinstance(asc, bool): raise Exception("Invalid type of argument 'asc'")
        # Member assignment.
        self.__field = Field(field)
        self.__asc = asc

    def get_field(self) -> Field: return self.__field
    def is_asc(self) -> bool: return self.__asc

    def __str__(self) -> str: return f"{self.__field.get_name()}, {self.__asc}"

class Order:
    """ An order definition. """
    def __init__(self):
        """ Creates a new order definition. """
        self.__segments: list = []

    def append_segment(self, field: Field, asc: bool = True):
        self.__segments.append(OrderSegment(field, asc))
    def get_segment(self, index: int) -> OrderSegment:
        if not isinstance(index, int): raise Exception("Invalid type for argument 'index'")
        return self.__segments[index]

    def __iter__(self): return self.__segments.__iter__()
    def __len__(self) -> int: return len(self.__segments)
    def __getitem__(self, index: int) -> OrderSegment:
        if not isinstance(index, int): raise Exception("Invalid type for 'index' argument")
        return self.__segments[index]
    def __str__(self) -> str:
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
        self.__table: Table or None = None

    def get_name(self) -> str or None: return self.__name
    def get_schema(self) -> str or None: return self.__schema
    def is_unique(self) -> bool:
        if self.__unique is None: return False
        return self.__unique
    def get_table(self) -> Table or None: return self.__table

    def set_name(self, name: str) -> None:
        if not isinstance(name, str): raise Exception("Invalid type for argument 'name'")
        self.__name = name
    def set_schema(self, schema: str) -> None:
        if not isinstance(schema, str): raise Exception("Invalid type for argument 'schema'")
        self.__schema = schema
    def set_unique(self, unique: bool) -> None:
        if not isinstance(unique, bool): raise Exception("Invalid type for argument 'unique'")
        self.__unique = unique
    def set_table(self, table: Table) -> None:
        if not isinstance(table, Table): raise Exception("Invalid type for argument 'table'")
        self.__table = table

    def __str__(self) -> str:
        _str_: str = self.get_name()
        if self.get_table() is not None:
            _str_ += " ON " + self.get_table().get_name()
        if self.is_unique(): _str_ += " UNIQUE"
        else: _str_ += " NOT UNIQUE"
        _str_ += " (" + super().__str__() + ")"
        return _str_

class Table:
    """
    A table definition.
    """
    def __init__(self):
        self.__name: str or None = None
        self.__alias: str or None = None
        self.__schema: str or None = None

        self.__fields: Fields = Fields()
        self.__primary_key: Index or None = None
        self.__indexes: list = []

    def append_field(self, field: Field) -> None:
        if not isinstance(field, Field): raise Exception("Invalid type for argument 'field'")
        self.__fields.append_field(field)

    def append_index(self, index: Index) -> None:
        if not isinstance(index, Index): raise Exception("Invalid type for argument 'index'")
        self.__indexes.append(index)

    def get_name(self): return self.__name
    def get_alias(self):
        if self.__alias is not None: return self.__alias
        return self.get_name()
    def get_schema(self): return self.__schema
    def get_name_schema(self):
        if self.get_name() is None: raise Exception("Table name not set")
        if self.get_schema() is not None: return self.get_name() + "." + self.get_schema()
        return self.get_name()
    def get_name_from(self): return self.get_name_schema() + " " + self.get_alias()

    def get_field(self, key: int or str) -> Field: return self.__fields.get_field(key)
    def get_indexes(self) -> list: return list(self.__indexes)
    def get_primary_key(self) -> Index or None: return self.__primary_key

    def set_name(self, name: str):
        if not isinstance(name, str): raise Exception("Argument name must be str")
        self.__name = name
    def set_alias(self, alias: str):
        if not isinstance(alias, str): raise Exception("Argument alias must be str")
        self.__alias = alias
    def set_schema(self, schema: str):
        if not isinstance(schema, str): raise Exception("Argument schema must be str")
        self.__schema = schema

    def validate_and_setup(self) -> None:
        """
        Setup and validate. Must be called after name, alias, schema, fields and indexes are set.
        """

        # Reset fields.
        self.__fields.__setup__()

        # Validate that fields are persistent.
        for field in self.__fields:
            if not field.is_persistent():
                raise Exception(f"Non persistent fields ({field}) not allowed in tables")

        # References of fields in the list of fields and in indexes are copies.
        # Ensure that all fields have not aliases or views. Set the table.
        for field in self.__fields:
            field.__alias = None
            field.__view = None
        for index in self.__indexes:
            for seg in range(len(index)):
                segment: OrderSegment = index.get_segment(seg)
                segment.get_field().__alias = None
                segment.get_field().__view = None

        # Validate that index fields are in the list of fields.
        for index in self.__indexes:
            for seg in range(len(index)):
                segment: OrderSegment = index.get_segment(seg)
                if not self.__fields.contains(segment.get_field()):
                    field: Field = segment.get_field()
                    raise Exception(f"Index field [{field}] not contained in the table")

        # Assign the table to fields.
        for field in self.__fields:
            field.set_table(self)

        # Create the names of the indexes and assign the table to the indexes and their fields.
        digits: int = max(len(str(len(self.__indexes))), 2)
        for ndx in range(len(self.__indexes)):
            index: Index = self.__indexes[ndx]
            name: str = self.get_name() + "_SK_" + str(ndx).ljust(digits, "0")
            index.set_name(name)
            index.set_table(self)
            index.set_schema(self.get_schema())
            for seg in range(len(index)):
                segment: OrderSegment = index.get_segment(seg)
                segment.get_field().set_table(self)

        # Build the primary key if there are primary key fields.
        # A default name and schema is set that can be changed later.
        pk_fields: list = self.__fields.get_primary_key_fields()
        if len(pk_fields) > 0:
            self.__primary_key = Index()
            index_name: str = self.get_name() + "_PK"
            self.__primary_key.set_name(index_name)
            self.__primary_key.set_unique(True)
            self.__primary_key.set_table(self)
            for i in range(len(pk_fields)):
                field: Field = pk_fields[i]
                self.__primary_key.append_segment(field)
        else:
            self.__primary_key = None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Table): return False
        return self.get_name_from() == other.get_name_from()

    def __str__(self) -> str: return self.get_name_from()

class RelationType(Enum, metaclass=EnumMeta):
    """ Relation type. """
    INNER = "INNER"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

class RelationSegment:
    """ A relation segment definition. """
    def __init__(self, local_field: Field, foreign_field: Field):
        if not isinstance(local_field, Field): raise Exception("Invalid type for local field")
        if not isinstance(foreign_field, Field): raise Exception("Invalid type for foreign field")
        self.__local_field = Field(local_field)
        self.__foreign_field = Field(foreign_field)

    def get_local_field(self) -> Field: return self.__local_field
    def get_foreign_field(self) -> Field: return self.__foreign_field

class Relation:
    """ A relation between two tables. """
    def __init__(self,
                 local_table: Table,
                 foreign_table: Table,
                 type=RelationType.LEFT):
        """
        Creates a new relation.
        :param local_table: The local table.
        :param foreign_table: The foreign table.
        """
        if not isinstance(local_table, Table): raise Exception("Invalid type for 'local_table'")
        if not isinstance(foreign_table, Table): raise Exception("Invalid type for 'foreign_table'")
        self.__local_table: Table = local_table
        self.__foreign_table: Table = foreign_table
        self.__segments: list = []
        self.__type: RelationType = type

    def add_segment(self, local_field: Field, foreign_field: Field):
        self.__segments.append(RelationSegment(local_field, foreign_field))
    def get_segment(self, index: int) -> RelationSegment:
        if not isinstance(index, int): raise Exception("Invalid type for argument 'index")
        return self.__segments[index]
    def get_local_table(self) -> Table: return self.__local_table
    def get_foreign_table(self) -> Table: return self.__foreign_table
    def get_type(self) -> RelationType: return self.__type

    def __iter__(self): return self.__segments.__iter__()
    def __len__(self) -> int: return len(self.__segments)
    def __getitem__(self, index: int) -> RelationSegment:
        if not isinstance(index, int): raise Exception("Invalid type for 'index' argument")
        return self.__segments[index]

class View:
    """ An SQL view. """
    def __init__(self):
        self.__master_table: Table or None = None
        self.__fields: Fields = Fields()
        self.__relations: list = []
        self.__group_by: list = []
        self.__order_by: Order = Order()

    def append_field(self, field: Field) -> None:
        self.__fields.append_field(field)
    def append_group_by_field(self, field: Field) -> None:
        if not isinstance(field, Field): raise Exception("Invalid type for argument 'field'")
        self.__group_by.append(Field(field))
    def append_order_by_field(self, field: Field, asc: bool = True) -> None:
        if not isinstance(field, Field): raise Exception("Invalid type for argument 'field'")
        self.__order_by.append_segment(field, asc)
    def append_relation(self, relation: Relation) -> None:
        if not isinstance(relation, Relation): raise Exception("Invalid type for argument 'relation'")
        self.__relations.append(relation)

    def set_master_table(self, table: Table) -> None:
        if not isinstance(table, Table): raise Exception("Invalid type for argument 'table'")
        self.__master_table = table

    def validate_and_setup(self) -> None:

        # Build the list with all involved tables.
        tables: list = []
        if self.__master_table is not None:
            tables.append(self.__master_table)
        for i in range(len(self.__relations)):
            relation: Relation = self.__relations[i]
            if relation.get_local_table() is not None:
                table: Table = relation.get_local_table()
                if table not in tables: tables.append(table)
            if relation.get_foreign_table() is not None:
                table: Table = relation.get_foreign_table()
                if table not in tables: tables.append(table)

        # Validate that all persistent fields belong to one of the tables.
        for i in range(len(self.__fields)):
            field: Field = self.__fields[i]
            if field.is_persistent() and field.get_table() is None:
                raise Exception(f"Field {field} has no table reference")
            ok_table: bool = False
            for table in tables:
                if field.get_table() == table:
                    ok_table = True
                    break
            if not ok_table:
                raise Exception(f"Field {field} does not belong to any related table")

        # Group by fields must be in the list of fields.
        for i in range(len(self.__group_by)):
            field: Field = self.__group_by[i]
            if not self.__fields.contains(field):
                raise Exception(f"Group by field {field} not contained in the field list")

        # Order by fields must be in the list of fields.
        for i in range(len(self.__order_by)):
            segment: OrderSegment = self.__order_by[i]
            field: Field = segment.get_field()
            if not self.__fields.contains(field):
                raise Exception(f"Order by field {field} not contained in the field list")

def create_field(name: str, type: Types, length: int or None = None, decimals: int or None = None) -> Field:
    """
    Create a basic field definition.
    :param name: The name.
    :param type: The type.
    :param length: Optional length.
    :param decimals: Optional decimals.
    :return: The field definition.
    """
    field: Field = Field()
    field.set_name(name)
    field.set_type(type)
    if length is not None:
        field.set_length(length)
    if decimals is not None:
        field.set_decimals(decimals)
    return field
