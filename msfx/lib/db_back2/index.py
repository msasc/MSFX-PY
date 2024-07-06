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
from msfx.lib.db_back2.order import Order
from msfx.lib import error_msg

class Table: pass

class Index(Order):
    """ An index of a table. """
    def __init__(self):
        super().__init__()
        self.__name = ""
        self.__description = ""
        self.__unique = False
        self.__table = None
        self.__schema = ""

    def get_name(self):
        return self.__name
    def set_name(self, name):
        if name is None or not isinstance(name, str):
            error = error_msg("type error", "name", type(name), (str,))
            raise TypeError(error)
        self.__name = name

    def get_description(self):
        return self.__description
    def set_description(self, description):
        if description is None or not isinstance(description, str):
            error = error_msg("type error", "description", type(description), (str,))
            raise TypeError(error)
        self.__description = description

    def is_unique(self):
        return self.__unique
    def set_unique(self, unique=False):
        if unique is None or not isinstance(unique, bool):
            error = error_msg("type error", "unique", type(unique), (bool,))
            raise TypeError(error)
        self.__unique = unique

    def get_table(self):
        return self.__table
    def set_table(self, table: Table):
        if table is not None:
            if type(table).__name__ != Table.__name__:
                error = error_msg("type error", "table", type(table).__name__, (Table.__name__,))
                raise TypeError(error)
            self.__table = table

    def get_schema(self):
        return self.__schema
    def set_schema(self, schema):
        if schema is None or not isinstance(schema, str):
            error = error_msg("type error", "schema", type(schema), (str,))
            raise TypeError(error)
        self.__schema = schema

    # noinspection PyDictCreation
    def to_dict(self):
        data = {}
        data["name"] = self.__name
        data["description"] = self.__description
        data["unique"] = self.__unique
        data["table"] = None if self.__table is None else self.__table.get_name()
        data["schema"] = self.__schema
        data |= super().to_dict()
        return data
