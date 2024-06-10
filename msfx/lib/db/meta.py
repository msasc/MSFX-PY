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

"""
Database metadata.
"""
from msfx.lib.db.types import Types

class Table: pass
class View: pass

class Column:
    """ A column of a table or view. """
    def __init__(self, column=None):
        self.__data = {}
        if isinstance(column, Column): self.__data |= column.__data

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

    def get_type(self) -> Types:
        type = self.__data.get("type")
        return type if isinstance(type, Types) else None
    def set_type(self, type: Types):
        self.__data["type"] = type

    def get_length(self) -> int:
        length = self.__data.get("length")
        return length if isinstance(length, int) else -1
    def set_length(self, length: int):
        self.__data["length"] = length

    def get_decimals(self) -> int:
        decimals = self.__data.get("decimals")
        return decimals if isinstance(decimals, int) else -1
    def set_decimals(self, decimals: int):
        self.__data["decimals"] = decimals

    def is_primary_key(self) -> bool:
        primary_key = self.__data.get("primary_key")
        return primary_key if isinstance(primary_key, bool) else False
    def set_primary_key(self, primary_key: bool):
        self.__data["primary_key"] = primary_key

    def get_header(self) -> str:
        header = self.__data.get("header")
        return header if isinstance(header, str) else ""
    def set_header(self, header: str):
        self.__data["header"] = header

    def get_label(self) -> str:
        label = self.__data.get("label")
        return label if isinstance(label, str) else ""
    def set_label(self, label: str):
        self.__data["label"] = label

    def get_description(self) -> str:
        description = self.__data.get("description")
        return description if isinstance(description, str) else ""
    def set_description(self, description: str):
        self.__data["description"] = description

    def get_table(self) -> Table:
        table = self.__data.get("table")
        return table if isinstance(table, Table) else None
    def set_table(self, table: Table):
        self.__data["table"] = table

    def get_view(self) -> View:
        view = self.__data.get("view")
        return view if isinstance(view, View) else None
    def set_view(self, view: View):
        self.__data["view"] = view

class Columns:
    def __init__(self):
        self.__columns = []
        self.__aliases = []
        self.__indexes = {}
