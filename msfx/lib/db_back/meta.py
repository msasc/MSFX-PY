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

"""
Database metadata.
"""
from decimal import Decimal

from msfx.lib.db_back.meta_shema import (
    COLUMN_SCHEMA,
    COLUMN_NAME, COLUMN_ALIAS,
    COLUMN_TYPE, COLUMN_LENGTH, COLUMN_DECIMALS,
    COLUMN_PRIMARY_KEY,
    COLUMN_HEADER, COLUMN_LABEL, COLUMN_DESCRIPTION,
    COLUMN_TABLE, COLUMN_VIEW,
    Table, View
)
from msfx.lib.db_back.types import Types
from msfx.lib.db_back.value import Value
from msfx.lib.util.generics import dict_set_value, dict_get_value

class Column:
    """ A column of a table or view. """
    def __init__(self, column=None, **kwargs):
        self.__data = {}
        if isinstance(column, Column):
            self.__data |= column.__data

    def get_name(self) -> str:
        return dict_get_value(self.__data, COLUMN_NAME, COLUMN_SCHEMA)
    def set_name(self, name: str):
        dict_set_value(self.__data, COLUMN_NAME, name, str)

    def get_alias(self) -> str:
        return dict_get_value(self.__data, COLUMN_ALIAS, COLUMN_SCHEMA)
    def set_alias(self, alias: str):
        dict_set_value(self.__data, COLUMN_ALIAS, alias, str)

    def get_type(self) -> Types:
        return dict_get_value(self.__data, COLUMN_TYPE, COLUMN_SCHEMA)
    def set_type(self, type: Types):
        dict_set_value(self.__data, COLUMN_TYPE, type, Types)

    def get_length(self) -> int:
        return dict_get_value(self.__data, COLUMN_LENGTH, COLUMN_SCHEMA)
    def set_length(self, length: int):
        dict_set_value(self.__data, COLUMN_LENGTH, length, int)

    def get_decimals(self) -> int:
        return dict_get_value(self.__data, COLUMN_DECIMALS, COLUMN_SCHEMA)
    def set_decimals(self, decimals: int):
        dict_set_value(self.__data, COLUMN_DECIMALS, decimals, int)

    def is_primary_key(self) -> bool:
        return dict_get_value(self.__data, COLUMN_PRIMARY_KEY, COLUMN_SCHEMA)
    def set_primary_key(self, primary_key: bool):
        dict_set_value(self.__data, COLUMN_PRIMARY_KEY, primary_key, int)

    def get_header(self) -> str:
        return dict_get_value(self.__data, COLUMN_HEADER, COLUMN_SCHEMA)
    def set_header(self, header: str):
        dict_set_value(self.__data, COLUMN_HEADER, header, int)

    def get_label(self) -> str:
        return dict_get_value(self.__data, COLUMN_LABEL, COLUMN_SCHEMA)
    def set_label(self, label: str):
        dict_set_value(self.__data, COLUMN_LABEL, label, int)

    def get_description(self) -> str:
        return dict_get_value(self.__data, COLUMN_DESCRIPTION, COLUMN_SCHEMA)
    def set_description(self, description: str):
        dict_set_value(self.__data, COLUMN_DESCRIPTION, description, int)

    def get_default_value(self) -> Value or None:
        type: Types = self.get_type()
        decs: int = self.get_decimals()
        decs = decs if decs >= 0 else 0
        if type is None: return None
        if type == Types.BOOLEAN: return Value(False)
        if type == Types.DECIMAL: return Value(round(Decimal(0), decs))
        if type == Types.INTEGER: return Value(int(0))
        if type == Types.FLOAT: return Value(float(0))
        if type == Types.COMPLEX: return Value(complex(0))
        if type == Types.DATE: return Value(Types.DATE)
        if type == Types.TIME: return Value(Types.TIME)
        if type == Types.DATETIME: return Value(Types.DATETIME)
        if type == Types.BINARY: return Value(bytes([]))
        if type == Types.STRING: return Value(str(""))
        if type == Types.LIST: return Value(list([]))
        if type == Types.DICTIONARY: return Value(dict({}))

    def get_table(self) -> Table:
        return self.__data.get(COLUMN_TABLE)
    def set_table(self, table: Table):
        dict_set_value(self.__data, COLUMN_TABLE, table, Table)

    def get_view(self) -> View:
        return self.__data.get(COLUMN_VIEW)
    def set_view(self, view: View):
        dict_set_value(self.__data, COLUMN_VIEW, view, View)

    def data(self) -> dict: return dict(self.__data)

    def __str__(self) -> str:
        result = "["
        comma = False
        for key in COLUMN_SCHEMA:
            value = self.__data.get(key)
            if value is not None:
                if comma: result += ", "
                result += f"{key}={value}"
                comma = True
        result += "]"
        return result

    def __repr__(self): return self.__str__()

class Columns:
    """ An ordered list of columns that can be efficiently accessed either by index or alias. """
    def __init__(self):
        self.__columns: list[Column] = []
        self.__aliases: list[str] = []
        self.__indexes: dict[str, int] = {}
        self.__pk_columns: list[Column] = []
        self.__default_values: list[Value] = []

    def add_column(self, column: Column, alias: str = None):
        # Validate.
        if column is None or not isinstance(column, Column):
            raise ValueError(f"Column can must be of type Column, not {type(column)}")
        # Create a copy.
        column = Column(column)
        if alias is not None: column.set_alias(alias)
        self.__columns.append(column)
        # Rebuild configurations.
        self.__setup()

    def remove_column(self, alias: str):
        index = self.__indexes.get(alias)
        if index is not None: del self.__columns[index]

    def index_of_column(self, alias: str) -> int:
        index = self.__indexes.get(alias)
        return -1 if index is None else index

    def get_column_by_alias(self, alias: str) -> Column or None:
        index = self.index_of_column(alias)
        if index < 0:
            raise ValueError(f"Invalid alias {alias}")
        return self.__columns[index]

    def get_column_by_index(self, index: int) -> Column or None:
        if not isinstance(index, int):
            raise ValueError(f"Index must be of type int, not {type(index)}")
        if index < 0:
            raise ValueError(f"Index must be >= 0, not {index}")
        if index >= len(self.__columns):
            raise ValueError(f"Index must be <= len(self.__columns)")
        return self.__columns[index]

    def get_columns(self) -> tuple[Column, ...]:
        return tuple(self.__columns)

    def get_pk_columns(self) -> tuple[Column, ...]:
        return tuple(self.__pk_columns)

    def get_aliases(self) -> tuple[str, ...]:
        return tuple(self.__aliases)

    def get_default_values(self) -> tuple[Value, ...]:
        return tuple(self.__default_values)

    def __setup(self):
        self.__aliases.clear()
        self.__indexes.clear()
        self.__pk_columns.clear()
        self.__default_values.clear()

        for i in range(len(self.__columns)):
            column = self.__columns[i]
            alias = column.get_alias()
            self.__aliases.append(alias)
            self.__indexes[alias] = i
            if column.is_primary_key():
                self.__pk_columns.append(column)
            self.__default_values.append(column.get_default_value())

    def __iter__(self):
        return self.__columns.__iter__()
    def __len__(self) -> int:
        return len(self.__columns)
    def __getitem__(self, index: int) -> Column:
        return self.get_column_by_index(index)

class Relation:
    """ A relation beween two tables. """
    def __init__(self, relation=None):
        self.__data = {}
        if isinstance(relation, Relation): self.__data |= relation.__data

    def get_local_table(self) -> Table or None:
        table = self.__data.get("local_table")
        if isinstance(table, Table):
            return table
        return None

    def get_foreign_table(self) -> Table or None:
        table = self.__data.get("foreign_table")
        if isinstance(table, Table):
            return table
        return None

class Order:
    """ Order definition. """
    def __init__(self, order=None):
        self.__segments: list[tuple[Column, bool]] = []
        if isinstance(order, Order):
            self.__segments += order.__segments

    def append(self, column: Column, asc: bool = True):
        if not isinstance(column, Column):
            raise ValueError("Column must be of type Column")
        self.__segments.append((Column(column), asc))

    def __iter__(self):
        return self.__segments.__iter__()
    def __len__(self) -> int:
        return len(self.__segments)

    def __getitem__(self, index: int) -> tuple[Column, bool] or None:
        if not isinstance(index, int):
            raise ValueError("Index must be of type int")
        if 0 <= index < len(self):
            return self.__segments[index]
        return None

    def __str__(self) -> str: return str(self.__segments)

class Index(Order):
    """ Index definition. """
    def __init__(self, index=None):
        super().__init__(self, index)
        self.__table: Table or None = None
        self.__primary_key: bool = False
        if isinstance(index, Index):
            self.__table = index.__table
            self.__primary_key = index.__primary_key

    def append(self, column: str or Column, asc: bool = True):
        if isinstance(column, Column):
            super().append(column, asc)
            return
        if isinstance(column, str):
            if self.__table is None:
                raise ValueError("Table must be set before appending using a column alias")
            column = self.__table.get_column(column)
            super().append(column, asc)

    def get_table(self) -> Table or None:
        return self.__table
    def set_table(self, table: Table):
        if not isinstance(table, Table):
            raise ValueError(f"Table must be of type {Table}")
        self.__table = table

# noinspection PyRedeclaration
class Table:
    """ A meta definition of a table. """
    def __init__(self, table=None):
        self.__data = {"columns": Columns(), "indexes": []}
        if isinstance(table, Table):
            self.__data |= table.__data

    def add_column(self, column: Column, alias: (str, None) = None):
        column.set_table(self)
        self.__data["columns"].add_column(column, alias)

    def get_column(self, key: (str, int)) -> Column or None:
        if not isinstance(key, (str, int)):
            raise ValueError("Key must be of type str or int")
        if isinstance(key, str):
            return self.__data["columns"].get_column_by_alias(key)
        if isinstance(key, int):
            return self.__data["columns"].get_column_by_index(key)
        return None

    def get_column_count(self) -> int:
        return len(self.__data["columns"])

    def add_index(self, index: Index):
        if not isinstance(index, Index):
            raise ValueError(f"Index must be of type {Index}")
        index.set_table(self)
        self.__data["indexes"].append(index)

    def get_index(self, index: int) -> Index:
        if not isinstance(index, int):
            raise ValueError(f"Index must be of type {int}")
        if index < 0 or index >= len(self.__data["indexes"]):
            raise ValueError(f"Index out of range")
        return self.__data["indexes"][index]

    def get_index_count(self):
        return len(self.__data["indexes"])

    def get_name(self) -> str:
        name = self.__data.get("name")
        return name if isinstance(name, str) else ""
    def set_name(self, name: str):
        self.__data["name"] = name

    def get_alias(self) -> str:
        alias = self.__data.get("alias")
        return alias if isinstance(alias, str) else self.get_name()
    def set_alias(self, alias: str):
        self.__data["alias"] = alias

    def get_schema(self) -> str:
        schema = self.__data.get("schema")
        return schema if isinstance(schema, str) else ""
    def set_schema(self, schema: str):
        self.__data["schema"] = schema
