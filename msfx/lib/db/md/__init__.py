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

from enum import Enum

from msfx.lib import round_dec
from msfx.lib.db import Types, Value
from msfx.lib.props import Properties

class ColumnProps(Enum):
    NAME = "NAME"
    ALIAS = "ALIAS"
    TYPE = "TYPE"
    LENGTH = "LENGTH"
    SCALE = "SCALE"
    PRIMARY_KEY = "PRIMARY_KEY"
    NULLABLE = "NULLABLE"
    UPPERCASE = "UPPERCASE"
    HEADER = "HEADER"
    LABEL = "LABEL"
    DESCRIPTION = "DESCRIPTION"
    TABLE = "TABLE"
    PROPERTIES = "PROPERTIES"
class ColumnListProps(Enum):
    COLUMNS = "COLUMNS"
    ALIASES = "ALIASES"
    INDEXES = "INDEXES"
    PK_COLUMNS = "PK_COLUMNS"
    DEFAULT_VALUES = "DEFAULT_VALUES"
class OrderProps(Enum):
    SEGMENTS = "SEGMENTS"
class IndexProps(Enum):
    NAME = "NAME"
    SCHEMA = "SCHEMA"
    DESCRIPTION = "DESCRIPTION"
    UNIQUE = "UNIQUE"
    TABLE = "TABLE"
    SEGMENTS = "SEGMENTS"
class ForeignKeyProps(Enum):
    NAME = "NAME"
    PERSISTENT = "PERSISTENT"
    ON_DELETE = "ON_DELETE"
    LOCAL_TABLE = "LOCAL_TABLE"
    FOREIGN_TABLE = "FOREIGN_TABLE"
    SEGMENTS = "SEGMENTS"
class TableProps(Enum):
    NAME = "NAME"
    ALIAS = "ALIAS"
    SCHEMA = "SCHEMA"
    DESCRIPTION = "DESCRIPTION"
    PERSISTENT = "PERSISTENT"
    PRIMARY_KEY = "PRIMARY_KEY"
    COLUMNS = "COLUMNS"
    INDEXES = "INDEXES"
    FOREIGN_KEYS = "FOREIGN_KEYS"
    PROPERTIES = "PROPERTIES"

class Column:
    """ Column metadata. """

    def __init__(self):
        self.__props = Properties()
        self.__props.set_props(ColumnProps.PROPERTIES, Properties())

    def copy(self):
        col = Column()
        col.__props = self.__props.copy()
        return col

    def get_name(self) -> str:
        return self.__props.get_string(ColumnProps.NAME)
    def get_alias(self) -> str:
        return self.__props.get_string(ColumnProps.ALIAS, self.get_name())
    def get_type(self) -> Types:
        return self.__props.get_any(ColumnProps.TYPE, Types.STRING)
    def get_length(self) -> int:
        return self.__props.get_integer(ColumnProps.LENGTH, -1)
    def get_scale(self) -> int:
        return self.__props.get_integer(ColumnProps.SCALE, -1)

    def is_primary_key(self) -> bool:
        return self.__props.get_bool(ColumnProps.PRIMARY_KEY, False)
    def is_nullable(self) -> bool:
        return self.__props.get_bool(ColumnProps.NULLABLE, True)
    def is_uppercase(self) -> bool:
        return self.__props.get_bool(ColumnProps.UPPERCASE, False)

    def get_header(self) -> str:
        return self.__props.get_string(ColumnProps.HEADER)
    def get_label(self) -> str:
        return self.__props.get_string(ColumnProps.LABEL)
    def get_description(self) -> str:
        return self.__props.get_string(ColumnProps.DESCRIPTION)

    def get_props(self) -> Properties:
        return self.__props.get_props(ColumnProps.PROPERTIES)

    def get_default_value(self) -> Value:
        type: Types = self.get_type()
        scale: int = self.get_scale()
        if type == Types.BOOLEAN: return Value(False)
        if type == Types.DECIMAL: return Value(round_dec(0, scale))
        if type == Types.INTEGER: return Value(int(0))
        if type == Types.FLOAT: return Value(float(0))
        if type == Types.COMPLEX: return Value(complex(0))
        if type == Types.DATE: return Value(Types.DATE)
        if type == Types.TIME: return Value(Types.TIME)
        if type == Types.DATETIME: return Value(Types.DATETIME)
        if type == Types.BINARY: return Value(bytes([]))
        if type == Types.STRING: return Value(str(""))
        if type == Types.LIST: return Value(list([]))
        if type == Types.DICT: return Value(dict({}))
        raise ValueError(f"Unsupported type {type}")

    def get_table_props(self) -> Properties:
        return self.__props.get_props(ColumnProps.TABLE)

    def set_name(self, name: str):
        self.__props.set_string(ColumnProps.NAME, name)
    def set_alias(self, alias: str):
        self.__props.set_string(ColumnProps.ALIAS, alias)
    def set_type(self, type: Types):
        self.__props.set_any(ColumnProps.TYPE, type)
    def set_length(self, length: int):
        self.__props.set_integer(ColumnProps.LENGTH, length)
    def set_scale(self, scale: int):
        self.__props.set_integer(ColumnProps.SCALE, scale)

    def set_primary_key(self, primary_key: bool):
        self.__props.set_bool(ColumnProps.PRIMARY_KEY, primary_key)
    def set_nullable(self, nullable: bool):
        self.__props.set_bool(ColumnProps.NULLABLE, nullable)
    def set_uppercase(self, uppercase: bool):
        self.__props.set_bool(ColumnProps.UPPERCASE, uppercase)

    def set_header(self, header: str):
        self.__props.set_string(ColumnProps.HEADER, header)
    def set_label(self, label: str):
        self.__props.set_string(ColumnProps.LABEL, label)
    def set_description(self, description: str):
        self.__props.set_string(ColumnProps.DESCRIPTION, description)

    def set_table_props(self, table_props: Properties):
        self.__props.set_props(ColumnProps.TABLE, table_props)

    def __str__(self) -> str:
        col = "[\""
        col += self.get_name()
        col += "\", \""
        col += self.get_type().name
        col += "\", "
        if self.get_length() >= 0: col += str(self.get_length())
        else: col += "--"
        col += ", "
        if self.get_scale() >= 0: col += str(self.get_scale())
        else: col += "--"
        col += ", \""
        col += self.get_header()
        col += "\"]"
        return col
    def __repr__(self):
        return self.__str__()
    """ End of class Column """
class ColumnList:
    """ Column list metadata. """
    def __init__(self, column_list_props: Properties = None):
        if isinstance(column_list_props, Properties):
            self.__read_only = True
            self.__props = column_list_props
        else:
            self.__read_only = False
            self.__props = Properties()
            self.__props.set_list(ColumnListProps.COLUMNS, [])
            self.__props.set_list(ColumnListProps.ALIASES, [])
            self.__props.set_dict(ColumnListProps.INDEXES, {})
            self.__props.set_list(ColumnListProps.PK_COLUMNS, [])
            self.__props.set_list(ColumnListProps.DEFAULT_VALUES, [])

    # Private properties.

    @property
    def __columns(self) -> list:
        return self.__props.get_list(ColumnListProps.COLUMNS)
    @property
    def __aliases(self) -> list:
        return self.__props.get_list(ColumnListProps.ALIASES)
    @property
    def __indexes(self) -> dict:
        return self.__props.get_dict(ColumnListProps.INDEXES)
    @property
    def __pk_columns(self) -> list:
        return self.__props.get_list(ColumnListProps.PK_COLUMNS)
    @property
    def __default_values(self) -> list:
        return self.__props.get_list(ColumnListProps.DEFAULT_VALUES)

    # Public properties.

    @property
    def columns(self):
        return ColumnList(self.__props)
    @property
    def aliases(self) -> list:
        return list(self.__aliases)
    @property
    def pk_columns(self) -> list:
        return list(self.__pk_columns)
    @property
    def default_values(self) -> list:
        return list(self.__default_values)

    def append(self, column: Column):
        if self.__read_only:
            raise PermissionError("Read-only status")
        if not isinstance(column, Column):
            raise TypeError("Arg column must be of type Column")
        self.__columns.append(column)
        self.__setup__()
    def remove(self, key: (int, str)):
        if self.__read_only:
            raise PermissionError("Read-only status")
        if not isinstance(key, (int, str)):
            raise TypeError("Arg key must be of type int or str")
        index = -1
        if isinstance(key, int):
            index = key
        if isinstance(key, str):
            index = self.index_of(key)
        if 0 <= index < len(self.__columns):
            del self.__columns[index]
            self.__setup__()
    def clear(self):
        if self.__read_only:
            raise PermissionError("Read-only status")
        self.__columns.clear()
        self.__setup__()

    def index_of(self, alias: str) -> int:
        if not isinstance(alias, str):
            raise TypeError("Arg alias must be of type str")
        index = self.__indexes.get(alias)
        return -1 if index is None else index
    def get_by_alias(self, alias: str) -> Column:
        if not isinstance(alias, str):
            raise TypeError("Arg alias must be of type str")
        index = self.index_of(alias)
        if index < 0:
            raise ValueError(f"Invalid alias {alias}")
        return self.__columns[index]
    def get_by_index(self, index: int) -> Column:
        if index is None or not isinstance(index, int):
            raise TypeError("Arg index must be of type int")
        if index < 0 or index >= len(self.__columns):
            raise ValueError("Index out of range")
        return self.__columns[index]

    def __setup__(self):
        self.__aliases.clear()
        self.__indexes.clear()
        self.__pk_columns.clear()
        self.__default_values.clear()

        for i in range(len(self.__columns)):
            column: Column = self.__columns[i]
            self.__aliases.append(column.get_alias())
            self.__indexes[column.get_alias()] = i
            if column.is_primary_key():
                self.__pk_columns.append(column)
            self.__default_values.append(column.get_default_value())
    """ End of class ColumnList """
class Order:
    """ An order definition. """
    def __init__(self):
        self.__props = Properties()
        self.__props.set_list(OrderProps.SEGMENTS, [])

    @property
    def __segments(self) -> list:
        return self.__props.get_list(OrderProps.SEGMENTS)

    def append(self, column: Column, ascending: bool = True):
        if not isinstance(column, Column):
            raise TypeError("Arg column must be of type Column")
        self.__segments.append((column, ascending))

    def __iter__(self):
        return self.__segments.__iter__()
    def __len__(self) -> int:
        return len(self.__segments)
    def __getitem__(self, index: int) -> (Column, bool):
        return self.__segments[index]
    """ End of class Order """
class Index:
    """ An index definition. """
    def __init__(self):
        self.__props = Properties()
        self.__props.set_list(IndexProps.SEGMENTS, [])

    @property
    def __segments(self) -> list:
        return self.__props.get_list(IndexProps.SEGMENTS)

    def append(self, column: Column, asc: bool = True):
        if not isinstance(column, Column):
            raise TypeError("Arg column must be of type Column")
        self.__segments.append((column, asc))

    def get_name(self) -> str:
        return self.__props.get_string(IndexProps.NAME)
    def get_schema(self) -> str:
        return self.__props.get_string(IndexProps.SCHEMA)
    def get_description(self) -> str:
        return self.__props.get_string(IndexProps.DESCRIPTION)
    def is_unique(self) -> bool:
        return self.__props.get_bool(IndexProps.UNIQUE)

    def get_table_props(self) -> Properties:
        return self.__props.get_props(IndexProps.TABLE)

    def set_name(self, name: str):
        self.__props.set_string(IndexProps.NAME, name)
    def set_schema(self, schema: str):
        self.__props.set_string(IndexProps.SCHEMA, schema)
    def set_description(self, description: str):
        self.__props.set_string(IndexProps.DESCRIPTION, description)
    def set_unique(self, unique: bool):
        self.__props.set_bool(IndexProps.UNIQUE, unique)

    def set_table_props(self, props: Properties):
        self.__props.set_props(IndexProps.TABLE, props)

    def __iter__(self): return (
        self.__segments.__iter__())
    def __len__(self) -> int:
        return len(self.__segments)
    def __getitem__(self, index: int) -> (Column, bool):
        return self.__segments[index]
    """ End of class Index """
class ForeignKey:
    """ A foreign key definition. """
    def __init__(self):
        self.__props = Properties()
        self.__props.set_list(ForeignKeyProps.SEGMENTS, [])

    @property
    def __segments(self) -> list:
        return self.__props.get_list(ForeignKeyProps.SEGMENTS)

    def get_name(self) -> str:
        return self.__props.get_string(ForeignKeyProps.NAME)
    def get_on_delete(self) -> str:
        return self.__props.get_string(ForeignKeyProps.ON_DELETE)
    def is_persistent(self) -> bool:
        return self.__props.get_bool(ForeignKeyProps.PERSISTENT)

    def get_local_table_props(self) -> Properties:
        return self.__props.get_props(ForeignKeyProps.LOCAL_TABLE)
    def get_foreign_table_props(self) -> Properties:
        return self.__props.get_props(ForeignKeyProps.FOREIGN_TABLE)

    def set_name(self, name: str):
        self.__props.set_string(ForeignKeyProps.NAME, name)
    def set_on_delete(self, on_delete: str):
        if not on_delete in ("CASCADE", "SET NULL", "SET DEFAULT", "NO ACTION", "RESTRICT"):
            raise ValueError(f"Invalid value for on_delete {on_delete}")
        self.__props.set_string(ForeignKeyProps.ON_DELETE, on_delete)
    def set_persistent(self, persistent: bool):
        self.__props.set_bool(ForeignKeyProps.PERSISTENT, persistent)

    def set_local_table_props(self, props: Properties):
        self.__props.set_props(ForeignKeyProps.LOCAL_TABLE, props)
    def set_foreign_table_props(self, props: Properties):
        self.__props.set_props(ForeignKeyProps.LOCAL_TABLE, props)

    def append(self, local_column: Column, foreign_column: Column):
        self.__segments.append((local_column, foreign_column))


    def __iter__(self):
        return self.__segments.__iter__()
    def __len__(self) -> int:
        return len(self.__segments)
    def __getitem__(self, index: int) -> (Column, Column):
        return self.__segments[index]
    """ End of class ForeignKey """
class Table:
    """ A table definition. """
    def __init__(self, props: Properties = None):
        self.__props = None
        if isinstance(props, Properties):
            self.__props = props
        else:
            self.__props = Properties()
            self.__props.set_any(TableProps.COLUMNS, ColumnList())
            self.__props.set_list(TableProps.INDEXES, [])
            self.__props.set_list(TableProps.FOREIGN_KEYS, [])
            self.__props.set_props(TableProps.PROPERTIES, Properties())

    # Private accessors to columns, indexes and foreign keys.

    @property
    def __columns(self) -> ColumnList:
        return self.__props.get_any(TableProps.COLUMNS)
    @property
    def __indexes(self) -> list:
        return self.__props.get_list(TableProps.INDEXES)
    @property
    def __foreign_keys(self) -> list:
        return self.__props.get_list(TableProps.FOREIGN_KEYS)

    # Public accessors to columns, indexes and foreign keys
    # that protect private members to be modified.

    @property
    def columns(self) -> ColumnList:
        return self.__columns.columns
    @property
    def indexes(self) -> list:
        return list(self.__indexes)
    @property
    def foreign_keys(self) -> list:
        return list(self.__foreign_keys)

    def get_name(self) -> str:
        return self.__props.get_string(TableProps.NAME)
    def get_alias(self) -> str:
        return self.__props.get_string(TableProps.ALIAS, self.get_name())
    def get_schema(self) -> str:
        return self.__props.get_string(TableProps.SCHEMA)
    def get_description(self) -> str:
        return self.__props.get_string(TableProps.DESCRIPTION)
    def is_persistent(self) -> bool:
        return self.__props.get_bool(TableProps.PERSISTENT)
    def get_primary_key(self) -> Index:
        return self.__props.get_any(TableProps.PRIMARY_KEY)

    def get_props(self) -> Properties:
        return self.__props.get_props(TableProps.PROPERTIES)

    def set_name(self, name: str):
        self.__props.set_string(TableProps.NAME, name)
    def set_alias(self, alias: str):
        self.__props.set_string(TableProps.ALIAS, alias)
    def set_schema(self, schema: str):
        self.__props.set_string(TableProps.SCHEMA, schema)
    def set_description(self, description: str):
        self.__props.set_string(TableProps.DESCRIPTION, description)
    def set_persistent(self, persistent: bool):
        self.__props.set_bool(TableProps.PERSISTENT, persistent)
    def set_primary_key(self, primary_key: Index):
        primary_key.set_table_props(self.__props)
        self.__props.set_any(TableProps.PRIMARY_KEY, primary_key)

    def append_column(self, column: Column):
        column.set_table_props(self.__props)
        self.__columns.append(column)
    def append_index(self, index: Index):
        index.set_table_props(self.__props)
        self.__indexes.append(index)
    def append_foreign_key(self, foreign_key: ForeignKey):
        foreign_key.set_local_table_props(self.__props)
        self.__foreign_keys.append(foreign_key)
