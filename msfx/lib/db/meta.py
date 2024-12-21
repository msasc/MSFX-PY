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

from enum import Enum

class ColumnKeys(Enum):
    NAME = "NAME"
    ALIAS = "ALIAS"
    TYPE = "TYPE"
    LENGTH = "LENGTH"
    DECIMALS = "DECIMALS"
    PRIMARY_KEY = "PRIMARY_KEY"
    NULLABLE = "NULLABLE"
    UPPERCASE = "UPPERCASE"
    HEADER = "HEADER"
    LABEL = "LABEL"
    DESCRIPTION = "DESCRIPTION"
    TABLE = "TABLE"
    VIEW = "VIEW"
    PROPERTIES = "PROPERTIES"
class ColumnListKeys(Enum):
    COLUMNS = "COLUMNS"
    ALIASES = "ALIASES"
    INDEXES = "INDEXES"
    PK_COLUMNS = "PK_COLUMNS"
    DEFAULT_VALUES = "DEFAULT_VALUES"

