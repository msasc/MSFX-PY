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
from msfx.lib.db.order import Order
from msfx.lib.db.table import Table
from msfx.lib.util.error import check_argument_type

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
        check_argument_type("name", name, (str,))
        self.__name = name

    def get_description(self):
        return self.__description
    def set_description(self, description):
        check_argument_type("description", description, (str,))
        self.__description = description

    def is_unique(self):
        return self.__unique
    def set_unique(self, unique=False):
        check_argument_type("unique", unique, (bool,))
        self.__unique = unique

    def get_table(self):
        return self.__table
    def set_table(self, table):
        check_argument_type("table", table, (Table,))
        self.__table = table

    def get_schema(self):
        return self.__schema
    def set_schema(self, schema):
        check_argument_type("schema", schema, (str,))
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
