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

from msfx.lib.db.json import JSON
from msfx.lib.db.value import Value
from msfx.lib.db.types import Types

js_src: JSON = JSON()
js_src.data()["name"] = "Miquel Sas"
print(js_src.dumps())
print(js_src)

js_dst: JSON = JSON(js_src.dumps())
print(js_dst)

val: Value = Value(js_dst)
print(val)

v2: Value = Value(Types.DATE)
print(v2.is_none())
