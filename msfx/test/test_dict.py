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
from msfx.lib.db.types import Types

def test_args(**kwargs):
    keys = {
        "first_name": str,
        "last_name": str,
        "age": int
    }
    data = {}
    for key, tp in keys.items():
        value = kwargs.get(key)
        if isinstance(value, tp):
            data[key] = value
    print(data)

test_args(first_name="Miquel", last_name="Sas", age=66)