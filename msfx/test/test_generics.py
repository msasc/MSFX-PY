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

from msfx.lib.db.meta_shema import COLUMN_SCHEMA
from msfx.lib.db.types import Types
from msfx.lib.util.generics import dict_create, dict_validate, dict_get_value

column = dict_create(COLUMN_SCHEMA)
print(column)

try:
    dict_validate(column, COLUMN_SCHEMA)
    print("Column is valid")
    dict_validate({}, COLUMN_SCHEMA, True)
    print("Empty dict valid")
except (KeyError, TypeError) as e:
    print(e)

SCHEMA: Dict[str, Union[str, int, bool]] = {
    "name": "Roger Moore",
    "alias": "Bond",
    "age": 40,
    "agent": True
}

print(dict_get_value({}, "name", SCHEMA))
print(dict_get_value({}, "alias", SCHEMA))