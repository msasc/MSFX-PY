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

from decimal import Decimal
from typing import Optional

from msfx.lib_back2.db_back2.types import Types
from msfx.lib_back2.db_back2.value import Value
from msfx.lib_back2 import error_msg

class Table: pass
class View: pass

class Column:
    """ A column of a table or view. """
    def __init__(self, column=None, **kwargs):
        self.__name = ""
        self.__alias = ""
        self.__type = None
        self.__length = -1
        self.__decimals = -1
        self.__primary_key = False
        self.__nullable = False
        self.__header = ""
        self.__label = ""
        self.__description = ""
        self.__uppercase = False
        self.__table = None
        self.__view = None
        if len(kwargs) > 0:
            self.__name = kwargs.get("name", "")
            self.__alias = kwargs.get("alias", "")
            self.__type = kwargs.get("type", None)
            self.__length = kwargs.get("length", -1)
            self.__decimals = kwargs.get("decimals", -1)
            self.__primary_key = kwargs.get("primary_key", False)
            self.__nullable = kwargs.get("nullable", False)
            self.__header = kwargs.get("header", "")
            self.__label = kwargs.get("label", "")
            self.__description = kwargs.get("description", "")
            self.__uppercase = kwargs.get("description", False)
            self.__table = kwargs.get("table", None)
            self.__view = kwargs.get("view", None)
        if isinstance(column, Column):
            self.__name = column.__name
            self.__alias = column.__alias
            self.__length = column.__length
            self.__decimals = column.__decimals
            self.__primary_key = column.__primary_key
            self.__nullable = column.__nullable
            self.__header = column.__header
            self.__label = column.__label
            self.__description = column.__description
            self.__uppercase = column.__uppercase
            self.__table = column.__table
            self.__view = column.__view

    def get_name(self) -> str:
        return self.__name
    def set_name(self, name: str):
        if name is not None:
            if not isinstance(name, str):
                error = error_msg("type error", "alias", type(name), (str,))
                raise TypeError(error)
            self.__name = name

    def get_alias(self) -> str:
        return self.__alias if len(self.__alias) > 0 else self.get_name()
    def set_alias(self, alias: str):
        if alias is not None:
            if not isinstance(alias, str):
                error = error_msg("type error", "alias", type(alias), (str,))
                raise TypeError(error)
            self.__alias = alias

    def get_type(self) -> Types:
        return self.__type
    def set_type(self, dbtype: Types):
        if dbtype is not None:
            if not isinstance(dbtype, Types):
                error = error_msg("type error", "vtype", type(dbtype), (Types,))
                raise TypeError(error)
            self.__type = dbtype

    def get_length(self) -> int:
        return self.__length
    def set_length(self, length: int):
        if length is not None:
            if not isinstance(length, int):
                error = error_msg("type error", "length", type(length), (int,))
                raise TypeError(error)
            self.__length = length if length > 0 else -1

    def get_decimals(self) -> int:
        return self.__decimals
    def set_decimals(self, decimals: int):
        if decimals is not None:
            if not isinstance(decimals, int):
                error = error_msg("type error", "decimals", type(decimals), (int,))
                raise TypeError(error)
            self.__decimals = decimals if decimals >= 0 else -1

    def is_primary_key(self) -> bool:
        return self.__primary_key
    def set_primary_key(self, primary_key: bool):
        if primary_key is not None:
            if not isinstance(primary_key, bool):
                error = error_msg("type error", "primay_key", type(primary_key), (bool,))
                raise TypeError(error)
            self.__primary_key = primary_key
            if primary_key: self.__nullable = False

    def is_nullable(self) -> bool:
        return self.__nullable
    def set_nullable(self, nullable: bool):
        if nullable is not None:
            if not isinstance(nullable, bool):
                error = error_msg("type error", "nullable", type(nullable), (bool,))
                raise TypeError(error)
            if self.__primary_key: nullable = False
            self.__nullable = nullable

    def is_uppercase(self) -> bool:
        return self.__uppercase
    def set_uppercase(self, uppercase: bool):
        if uppercase is not None:
            if not isinstance(uppercase, bool):
                error = error_msg("type error", "uppercase", type(uppercase), (bool,))
                raise TypeError(error)
            self.__uppercase = uppercase

    def get_header(self) -> str:
        return self.__header
    def set_header(self, header: str):
        if header is not None:
            if not isinstance(header, str):
                error = error_msg("type error", "header", type(header), (str,))
                raise TypeError(error)
            self.__header = header

    def get_label(self) -> str:
        return self.__label
    def set_label(self, label: str):
        if label is not None:
            if not isinstance(label, str):
                error = error_msg("type error", "label", type(label), (str,))
                raise TypeError(error)
            self.__label = label

    def get_description(self) -> str:
        return self.__description
    def set_description(self, description: str):
        if description is not None:
            if not isinstance(description, str):
                error = error_msg("type error", "description", type(description), (str,))
                raise TypeError(error)
            self.__description = description

    def get_default_value(self) -> Optional[Value]:
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
        raise ValueError(f"Unsupported type {type}")

    def get_table(self) -> Optional[Table]:
        return self.__table
    def set_table(self, table: Table):
        if table is not None:
            received = type(table).__name__
            expected = Table.__name__
            if received != expected:
                error = error_msg("type name error", "table", received, (expected,))
                raise TypeError(error)
            self.__table = table

    def get_view(self) -> Optional[View]:
        return self.__view
    def set_view(self, view: View):
        if view is not None:
            received = type(view).__name__
            expected = View.__name__
            if received != expected:
                error = error_msg("type name error", "view", received, (expected,))
                raise TypeError(error)
            self.__view = view

    def to_dict(self) -> dict:
        data = {}
        if self.__name != "": data["name"] = self.__name
        if self.__alias != "": data["alias"] = self.__alias
        if self.__type is not None: data["type"] = self.__type.name
        if self.__length >= 0: data["length"] = self.__length
        if self.__decimals >= 0: data["decimals"] = self.__decimals
        if self.__primary_key: data["primary_key"] = self.__primary_key
        if self.__uppercase: data["uppercase"] = self.__uppercase
        if self.__header != "": data["header"] = self.__header
        if self.__label != "": data["label"] = self.__label
        if self.__description != "": data["description"] = self.__description
        if self.__table is not None: data["table"] = self.__table.get_name()
        if self.__view is not None: data["view"] = self.__view.get_name()
        return data

    def __str__(self) -> str:
        return str(self.to_dict())
    def __repr__(self):
        return self.__str__()

class ColumnList:
    """ An ordered list of columns that can be efficiently accessed either by index or alias. """
    def __init__(self, column_list=None):
        self.__columns = []
        self.__aliases = []
        self.__indexes = {}
        self.__pk_columns = []
        self.__default_values = []
        if column_list is not None and isinstance(column_list, ColumnList):
            self.__columns |= column_list.__columns
            self.__setup()

    def append(self, column: Column):
        if column is None or not isinstance(column, Column):
            error = error_msg("type error", "column", type(column), (Column,))
            raise TypeError(error)
        self.__columns.append(Column(column))
        self.__setup()

    def remove(self, key: (int, str)):
        if key is None or not isinstance(key, (int, str)):
            error = error_msg("type error", "key", type(key), (int, str))
            raise TypeError(error)
        index = -1
        if isinstance(key, int): index = key
        if isinstance(key, str): index = self.index_of(key)
        if 0 <= index < len(self.__columns):
            del self.__columns[index]
            self.__setup()

    def clear(self):
        self.__columns.clear()
        self.__setup()

    def index_of(self, alias: str) -> int:
        if alias is None or not isinstance(alias, str):
            error = error_msg("type error", "alias", type(alias), (str,))
            raise TypeError(error)
        index = self.__indexes.get(alias)
        return -1 if index is None else index

    def get_by_alias(self, alias: str) -> Column:
        if alias is None or not isinstance(alias, str):
            error = error_msg("type error", "alias", type(alias), (str,))
            raise TypeError(error)
        index = self.index_of(alias)
        if index < 0: raise ValueError(f"Invalid alias {alias}")
        return self.__columns[index]

    def get_by_index(self, index: int) -> Column:
        if index is None or not isinstance(index, int):
            error = error_msg("type error", "index", type(index), (int,))
            raise TypeError(error)
        if index < 0:
            error = error_msg("value error", "index", "< 0", (">= 0",))
            raise ValueError(error)
        if index >= len(self.__columns):
            error = error_msg("value error", "index", ">= len(columns)", ("< len(columns)",))
            raise ValueError(error)
        return self.__columns[index]

    def columns(self) -> list: return list(self.__columns)
    def aliases(self) -> list: return list(self.__aliases)
    def pk_columns(self) -> list: return list(self.__pk_columns)
    def default_values(self) -> list: return list(self.__default_values)

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

    def to_dict(self):
        data = {}
        columns = []
        for column in self.__columns:
            columns.append(column.get_name())
        data["columns"] = columns
        data["aliases"] = self.__aliases
        data["indexes"] = self.__indexes
        pk_columns = []
        for column in self.__pk_columns:
            pk_columns.append(column.get_name())
        data["pk_columns"] = pk_columns
        data["default_values"] = self.__default_values
        return data

    def __str__(self) -> str:
        return str(self.to_dict())
    def __repr__(self):
        return self.__str__()
    def __iter__(self):
        return self.__columns.__iter__()
    def __len__(self) -> int:
        return len(self.__columns)
    def __getitem__(self, index: int) -> Column:
        return self.get_by_index(index)
