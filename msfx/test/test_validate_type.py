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

from typing import Any, Type

info = {}

def set_value(data: dict, key: str, value: Any, expected_type: Type[Any]):
    if not isinstance(value, expected_type):
        raise ValueError(f"value must be of type {expected_type.__name__}")
    data[key] = value

# Example usage
try:
    set_value(info, "name", "example", str)
    print(info)  # Should print: {'name': 'example'}

    set_value(info, "length", 10, int)
    print(info)  # Should print: {'name': 'example', 'length': 10}

    set_value(info, "active", True, bool)
    print(info)  # Should print: {'name': 'example', 'length': 10, 'active': True}

    set_value(info, "invalid", "string", int)  # Should raise ValueError
except ValueError as e:
    print(e)  # Prints the exception message

set_value(info, "invalid", "string", int)  # Should raise ValueError
