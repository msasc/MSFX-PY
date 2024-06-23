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
from typing import Optional

from msfx.lib.util.generics import SCHEMA_TYPE, SCHEMA_DEFAULT

class Value: pass
class Table: pass
class View: pass

""" Column schema keys and default values. """

COLUMN_NAME = "name"
COLUMN_ALIAS = "alias"
COLUMN_TYPE = "type"
COLUMN_LENGTH = "length"
COLUMN_DECIMALS = "decimals"
COLUMN_PRIMARY_KEY = "primary_key"
COLUMN_HEADER = "header"
COLUMN_LABEL = "label"
COLUMN_DESCRIPTION = "description"
COLUMN_TABLE = "table"
COLUMN_VIEW = "view"

COLUMN_SCHEMA = {
    COLUMN_NAME: {SCHEMA_TYPE: str, SCHEMA_DEFAULT: ""},
    COLUMN_ALIAS: {SCHEMA_TYPE: str, SCHEMA_DEFAULT: ""},
    COLUMN_TYPE: {SCHEMA_TYPE: str, SCHEMA_DEFAULT: None},
    COLUMN_LENGTH: {SCHEMA_TYPE: int, SCHEMA_DEFAULT: -1},
    COLUMN_DECIMALS: {SCHEMA_TYPE: int, SCHEMA_DEFAULT: -1},
    COLUMN_PRIMARY_KEY: {SCHEMA_TYPE: bool, SCHEMA_DEFAULT: False},
    COLUMN_HEADER: {SCHEMA_TYPE: str, SCHEMA_DEFAULT: ""},
    COLUMN_LABEL: {SCHEMA_TYPE: str, SCHEMA_DEFAULT: ""},
    COLUMN_DESCRIPTION: {SCHEMA_TYPE: str, SCHEMA_DEFAULT: ""},
    COLUMN_TABLE: {SCHEMA_TYPE: Optional[Table], SCHEMA_DEFAULT: None},
    COLUMN_VIEW: {SCHEMA_TYPE: Optional[View], SCHEMA_DEFAULT: None}
}

""" ColumnList schema keys and default values. """

COLUMNLIST_COLUMNS = "columns"
COLUMNLIST_ALIASES = "aliases"
COLUMNLIST_INDEXES = "indexes"
COLUMNLIST_PK_COLUMNS = "pk_columns"
COLUMNLIST_DEFAULT_VALUES = "default_values"

COLUMNLIST_SCHEMA = {
    COLUMNLIST_COLUMNS: {SCHEMA_TYPE: list, SCHEMA_DEFAULT: []},
    COLUMNLIST_ALIASES: {SCHEMA_TYPE: list, SCHEMA_DEFAULT: []},
    COLUMNLIST_INDEXES: {SCHEMA_TYPE: dict, SCHEMA_DEFAULT: {}},
    COLUMNLIST_PK_COLUMNS: {SCHEMA_TYPE: list, SCHEMA_DEFAULT: []},
    COLUMNLIST_DEFAULT_VALUES: {SCHEMA_TYPE: list, SCHEMA_DEFAULT: []}
}