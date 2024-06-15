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
from typing import Dict, Union

from msfx.lib.db.schema import COLUMN_SCHEMA, COLUMN_NAME
from msfx.lib.db.types import Types
from msfx.lib.util.generics import dict_create_default, dict_create_args, dict_validate, dict_get_value

column_data = dict_create_default(COLUMN_SCHEMA)
print(column_data)

try:
    dict_validate(column_data, COLUMN_SCHEMA)
    print("column data is valid")
    dict_validate({}, COLUMN_SCHEMA, True)
    print("Empty dict valid")
except (KeyError, TypeError) as e:
    print(e)

value = dict_get_value({}, COLUMN_NAME, COLUMN_SCHEMA)
print(value)

column_data = dict_create_args(COLUMN_SCHEMA, name="CARTICLE", type=Types.STRING)
print(column_data)
