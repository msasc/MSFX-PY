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

from decimal import Decimal

from msfx.lib.db.types import Types
from msfx.lib.db.value import Value
from msfx.lib.util.error import check_argument_type, check_argument_value

class Column:
    """ A column of a table or view. """
    def __init__(self, column=None, **kwargs):
        self.__name = ""
        self.__alias = ""
        self.__type = None
        self.__length = -1
        self.__decimals = -1
        self.__primary_key = False
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
            self.__header = column.__header
            self.__label = column.__label
            self.__description = column.__description
            self.__uppercase = column.__uppercase
            self.__table = column.__table
            self.__view = column.__view

    def get_name(self):
        return self.__name
    def set_name(self, name):
        self.__name = name if isinstance(name, str) else ""

    def get_alias(self):
        return self.__alias if len(self.__alias) > 0 else self.get_name()
    def set_alias(self, alias):
        self.__alias = alias if isinstance(alias, str) else ""

    def get_type(self):
        return self.__type
    def set_type(self, type):
        self.__type = type if isinstance(type, Types) else None

    def get_length(self):
        return self.__length
    def set_length(self, length: int):
        self.__length = length if isinstance(length, int) else -1

    def get_decimals(self):
        return self.__decimals
    def set_decimals(self, decimals):
        self.__decimals = decimals if isinstance(decimals, int) else -1

    def is_primary_key(self):
        return self.__primary_key
    def set_primary_key(self, primary_key):
        self.__primary_key = primary_key if isinstance(primary_key, bool) else False

    def is_uppercase(self):
        return self.__uppercase
    def set_uppercase(self, uppercase):
        self.__uppercase = uppercase if isinstance(uppercase, bool) else False

    def get_header(self):
        return self.__header
    def set_header(self, header):
        self.__header = header if isinstance(header, str) else ""

    def get_label(self):
        return self.__label
    def set_label(self, label):
        self.__label = label if isinstance(label, str) else ""

    def get_description(self):
        return self.__description
    def set_description(self, description):
        self.__description = description if isinstance(description, bool) else ""

    def get_default_value(self):
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

    def get_table(self):
        return self.__table
    def set_table(self, table):
        self.__table = table

    def get_view(self):
        return self.__view
    def set_view(self, view):
        self.__view = view

    def to_dict(self):
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
        if column_list is not None:
            check_argument_type('column_list', column_list, ColumnList)

    def append_column(self, column):
        check_argument_type("column", column, (Column,))
        self.__columns.append(Column(column))
        self.__setup()

    def remove_column(self, key):
        check_argument_type("key", key, (int, str))
        index = -1
        if isinstance(key, int): index = key
        if isinstance(key, str): index = self.index_of_column(key)
        if 0 <= index < len(self.__columns):
            del self.__columns[index]
            self.__setup()

    def clear_columns(self):
        self.__columns.clear()
        self.__setup()

    def index_of_column(self, alias):
        check_argument_type('alias', alias, (str,))
        index = self.__indexes.get(alias)
        return -1 if index is None else index

    def get_column_by_alias(self, alias):
        check_argument_type('alias', alias, (str,))
        index = self.index_of_column(alias)
        if index < 0: raise ValueError(f"Invalid alias {alias}")
        return self.__columns[index]

    def get_column_by_index(self, index):
        check_argument_type("index", index, (int,))
        check_argument_value("index", index >= 0, index,">= 0")
        check_argument_value("index", index < 0, index >= len(self.get_columns()),"< len(columns)")
        return self.get_columns()[index]

    def get_columns(self): return list(self.__columns)
    def get_aliases(self): return list(self.__aliases)
    def get_pk_columns(self): return list(self.__pk_columns)
    def get_default_values(self): return list(self.__default_values)

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
        return self.get_column_by_index(index)
