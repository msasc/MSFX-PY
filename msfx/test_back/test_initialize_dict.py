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
from typing import Dict, Any, Union

from msfx.test_back.test_validate_dict import Types

def dict_data(schema: Dict[str, Any]) -> Dict[str, Any]:
    return {key: value for key, value in schema.items()}

# Example schema with default values
COLUMN_KEYS: Dict[str, Union[str, Types, int, bool]] = {
    "name": "",
    "alias": "",
    "type": Types.NONE,
    "length": -1,
    "decimals": -1,
    "primary_key": False,
    "header": "",
    "label": "",
    "decription": ""  # Assuming this is intended to be "description"
}

# Example usage
initial_data = dict_data(COLUMN_KEYS)
# print(initial_data)
