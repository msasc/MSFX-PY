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

class Table: pass

class Column:
    """ A column of a table or view. """
    def __init__(self):
        self.__data = {}

    def get_name(self) -> str:
        name = self.__data.get("name")
        return name if isinstance(name, str) else ""
    def set_name(self, name: str):
        self.__data["name"] = name

    def get_table(self) -> Table:
        table = self.__data.get("table")
        return table if isinstance(table, Table) else None
    def set_table(self, table: Table):
        self.__data["table"] = table

# noinspection PyRedeclaration
class Table:
    """ A meta definition of a table. """
    def __init__(self):
        self.__data = {}

    def add_column(self, column: Column):
        column.set_table(self)
        columns = self.__data.get("columns")
        if not isinstance(column, list):
            columns = []
            self.__data["columns"] = columns
        columns.append(column)
