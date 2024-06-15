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
from typing import Dict, Union, List

from msfx.lib.db.types import Types

class Column: pass
class Table: pass
class Value: pass
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

COLUMN_SCHEMA: Dict[str, Union[str, Types, int, bool]] = {
    COLUMN_NAME: "",
    COLUMN_ALIAS: "",
    COLUMN_TYPE: Types.NONE,
    COLUMN_LENGTH: -1,
    COLUMN_DECIMALS: -1,
    COLUMN_PRIMARY_KEY: False,
    COLUMN_HEADER: "",
    COLUMN_LABEL: "",
    COLUMN_DESCRIPTION: "",
    COLUMN_TABLE: None,
    COLUMN_VIEW: None
}

""" List of columns schema keys and default values. """

COLUMNS_COLUMNS = "columns"
COLUMNS_ALIASES = "aliases"
COLUMNS_INDEXES = "indexes"

COLUMNS_SCHEMA: Dict[str, Union[List[str], Dict[str, int]]] = {
    COLUMNS_COLUMNS: [],
    COLUMNS_ALIASES: [],
    COLUMNS_INDEXES: {}
}