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
from msfx.lib.db.column import ColumnList, Column
from msfx.lib.util.error import check_argument_type

class Table:
    """ A table definition. """
    def __init__(self):
        self.__name = ""
        self.__alias = ""

        self.__title = ""
        self.__description = ""

        self.__columns = ColumnList()

        self.__primary_key = None
        self.__indexes = []
        self.__foreign_keys = []

        self.__schema = ""
        self.__peristent_constraints = False

    def append_column(self, column):
        column.set_table(self)
        self.__columns.append_column(column)
    def remove_column(self, key):
        self.__columns.remove_column(key)
    def index_of_column(self, alias):
        return self.__columns.index_of_column(alias)
    def get_column_by_alias(self, alias):
        return self.__columns.get_column_by_alias(alias)
    def get_column_by_index(self, index):
        return self.__columns.get_column_by_index(index)
    def get_column_count(self):
        return len(self.__columns)

    def get_name(self):
        return self.__name
    def set_name(self, name):
        check_argument_type("name", name, (str,))
        self.__name = name

    def get_alias(self):
        return self.__alias
    def set_alias(self, alias):
        check_argument_type("alias", alias, (str,))
        self.__alias = alias

    def get_title(self):
        return self.__title
    def set_title(self, title):
        check_argument_type("title", title, (str,))
        self.__title = title

    def get_description(self):
        return self.__description
    def set_description(self, description):
        check_argument_type("description", description, (str,))
        self.__description = description

    def get_primary_key(self):
        return self.__primary_key
    def set_primary_key(self, primary_key):
        self.__primary_key = primary_key

    def append_index(self, index):
        self.__indexes.append(index)
    def clear_indexes(self):
        self.__indexes.clear()

    def append_foreign_key(self, foreign_key):
        self.__foreign_keys.append(foreign_key)
    def clear_foreign_keys(self):
        self.__foreign_keys.clear()


class TableLink:
    """ A link between two tables. """
    def __init__(self):
        self.__local_table = None
        self.__foreign_table = None
        self.__segments = []

    def get_local_table(self):
        return self.__local_table
    def set_local_table(self, local_table):
        check_argument_type("local_table", local_table, (Table,))
        self.__local_table = local_table

    def get_foreign_table(self):
        return self.__foreign_table
    def set_foreign_table(self, foreign_table):
        check_argument_type("foreign_table", foreign_table, (Table,))
        self.__foreign_table = foreign_table

    def append_segment(self, local_column, foreign_column):
        check_argument_type("local_column", local_column, (Column,))
        check_argument_type("foreign_column", foreign_column, (Column,))
        self.__segments.append({"local_column": local_column, "foreign_column": foreign_column})

    def clear_segment(self):
        self.__segments.clear()

    def to_dict(self):
        data = {}
        if self.__local_table is not None:
            data["local_table"] = self.__local_table.get_name()
        if self.__foreign_table is not None:
            data["foreign_table"] = self.__foreign_table.get_name()
        segments = []
        for segment in self.__segments:
            local_column = segment["local_column"]
            foreign_column = segment["foreign_column"]
            short_segment = {"local_column": local_column.get_name(), "foreign_column": foreign_column}
            segments.append(short_segment)
        data["segments"] = segments
        return data

    def __iter__(self):
        return self.__segments.__iter__()
    def __len__(self) -> int:
        return len(self.__segments)
    def __getitem__(self, index) -> {}:
        check_argument_type("index", index, (int,))
        if 0 <= index < len(self):
            return self.__segments[index]
        return None
    def __str__(self) -> str:
        return str(self.to_dict())
    def __repr__(self):
        return self.__str__()
