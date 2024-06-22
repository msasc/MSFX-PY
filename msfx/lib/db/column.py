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

from msfx.lib.db import BOOLEAN, DECIMAL, INTEGER, FLOAT, COMPLEX, DATE, TIME, DATETIME, BINARY, STRING, JSON
from msfx.lib.util import json

class Column:

    NAME = "name"
    ALIAS = "alias"
    TYPE = "type"
    LENGTH = "length"
    DECIMALS = "decimals"
    PRIMARY_KEY = "primary_key"
    NULLABLE = "nullable"
    HEADER = "header"
    LABEL = "label"
    DESCRIPTION = "description"
    UPPERCASE  = "uppercase"

    def __init__(self, column=None, **kwargs):
        self.__data = {}

    def get_name(self) -> str:
        return json.get_string(self.__data, Column.NAME, "")
    def set_name(self, name: str):
        json.put_string(self.__data, Column.NAME, name)

    def get_alias(self) -> str:
        alias = json.get_string(self.__data, Column.ALIAS, "")
        if alias == "": return self.get_name()
    def set_alias(self, alias: str):
        json.put_string(self.__data, Column.ALIAS, alias)
