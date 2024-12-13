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

from msfx.lib_back.db_back2.column import ColumnList, Column
from msfx.lib_back.db_back2.index import Index
from msfx.lib_back import error_msg

class ColumnListTable(ColumnList):
    def __init__(self, table):
        super().__init__()
        self.__table = table

    def append(self, column: Column):
        column.set_table(self.__table)
        super().append(column)

class Table:
    """ A table definition. """
    def __init__(self):
        self.__name = ""
        self.__alias = ""

        self.__title = ""
        self.__description = ""

        self.__columns = ColumnListTable(self)

        self.__primary_key = None
        self.__indexes = []
        self.__foreign_keys = []

        self.__schema = ""
        self.__peristent_constraints = False
        self.__trace_table = False

    def columns(self) -> ColumnListTable:
        return self.__columns

    def get_name(self):
        return self.__name
    def set_name(self, name):
        if name is not None:
            if not isinstance(name, str):
                error = error_msg("type error", "name", type(name), (str,))
                raise TypeError(error)
            self.__name = name

    def get_alias(self):
        return self.__alias
    def set_alias(self, alias):
        if alias is not None:
            if not isinstance(alias, str):
                error = error_msg("type error", "alias", type(alias), (str,))
                raise TypeError(error)
            self.__alias = alias

    def get_title(self):
        return self.__title
    def set_title(self, title):
        if title is not None:
            if not isinstance(title, str):
                error = error_msg("type error", "title", type(title), (str,))
                raise TypeError(error)
            self.__title = title

    def get_description(self):
        return self.__description
    def set_description(self, description):
        if description is not None:
            if not isinstance(description, str):
                error = error_msg("type error", "description", type(description), (str,))
                raise TypeError(error)
            self.__description = description

    def get_primary_key(self):
        if self.__primary_key is None:
            pk_columns = self.columns().pk_columns()
            if len(pk_columns) > 0 and len(self.__name) > 0:
                pk = Index()
                pk.set_name(self.__name + "_PK")
                pk.set_schema(self.__schema)
                pk.set_table(self)
                for column in pk_columns:
                    pk.append(column)
                self.__primary_key = pk
        return self.__primary_key

    def set_primary_key(self, primary_key):
        if primary_key is not None:
            if type(primary_key).__name__ != "Index":
                error = error_msg("type name error", "index", type(primary_key).__name__, ("Index",))
                raise TypeError(error)
            # TODO Validate that columns of the index are columns of this table
            primary_key.set_table(self)
            self.__primary_key = primary_key

    def append_index(self, index):
        if index is not None:
            if type(index).__name__ != "Index":
                error = error_msg("type name error", "index", type(index).__name__, ("Index",))
                raise TypeError(error)
            # TODO Validate that columns of the index are columns of this table
            index.set_table(self)
            self.__indexes.append(index)
    def clear_indexes(self):
        self.__indexes.clear()
    def get_indexes(self):
        return list(self.__indexes)

    def append_foreign_key(self, foreign_key):
        if foreign_key is not None:
            if type(foreign_key).__name__ != "ForeignKey":
                error = error_msg("type name error", "table", type(foreign_key).__name__, ("ForeignKey",))
                raise TypeError(error)
            # TODO Validate that local columns of the foreign key are columns of this table.
            foreign_key.set_local_table(self)
            self.__foreign_keys.append(foreign_key)
    def clear_foreign_keys(self):
        self.__foreign_keys.clear()
    def get_foreign_keys(self):
        return list(self.__foreign_keys)

    def to_dict(self):
        data = {}
        data["name"] = self.get_name()
        data["alias"] = self.get_alias()
        data["title"] = self.get_title()
        data["description"] = self.get_description()
        data["primary_key"] = self.get_primary_key()
        return data

    def __str__(self) -> str:
        return str(self.to_dict())
    def __repr__(self):
        return self.__str__()

class TableLink:
    """ A link between two tables. """
    def __init__(self):
        self.__local_table = None
        self.__foreign_table = None
        self.__segments = []

    def get_local_table(self):
        return self.__local_table
    def set_local_table(self, local_table):
        if local_table is None or not isinstance(local_table, Table):
            error = error_msg("type error", "local_table", type(local_table), (Table,))
            raise TypeError(error)
        self.__local_table = local_table

    def get_foreign_table(self):
        return self.__foreign_table
    def set_foreign_table(self, foreign_table):
        if foreign_table is None or not isinstance(foreign_table, Table):
            error = error_msg("type error", "foreign_table", type(foreign_table), (Table,))
            raise TypeError(error)
        self.__foreign_table = foreign_table

    def append_segment(self, local_column, foreign_column):
        if local_column is None or not isinstance(local_column, Column):
            error = error_msg("type error", "local_column", type(local_column), (Column,))
            raise TypeError(error)
        if foreign_column is None or not isinstance(foreign_column, Column):
            error = error_msg("type error", "foreign_column", type(foreign_column), (Column,))
            raise TypeError(error)
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
            short_segment = {"local_column": local_column.get_name(), "foreign_column": foreign_column.get_name()}
            segments.append(short_segment)
        data["segments"] = segments
        return data

    def __iter__(self):
        return self.__segments.__iter__()
    def __len__(self) -> int:
        return len(self.__segments)
    def __getitem__(self, index: int) -> {}:
        if index is None or not isinstance(index, int):
            error = error_msg("type error", "index", type(index), (int,))
            raise TypeError(error)
        if 0 <= index < len(self):
            return self.__segments[index]
        return None
    def __str__(self) -> str:
        return str(self.to_dict())
    def __repr__(self):
        return self.__str__()
