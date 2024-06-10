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

from datetime import date, datetime
from msfx.lib.db_back.json_back import JSON
from msfx.lib.db_back.value import Value
from msfx.lib.db_back.types import Types

js_src: JSON = JSON()
js_src.data()["name"] = "Miquel Sas"
print(js_src.dumps())
print(js_src)

js_dst: JSON = JSON(js_src.dumps())
print(js_dst)

v1: Value = Value(js_dst)
print(v1)

v2: Value = Value(Types.DATE)
print(v2.is_none())

v3: Value = Value("A")
v4: Value = Value("A")
v5: Value = Value(date(2022, 5, 12))

print(v3 == v4)
print(Value(10) == Value(10.00))

print(v3.is_comparable("A"))
print(v3.is_comparable(js_dst))
print(v3.is_comparable(Value(2)))
print(v3.is_comparable(Value(True)))
print(v5)
print(v5.get_date().year)
print(v5.get_date().month)
print(v5.get_date().day)
print(v5.get_date())

d: date = v5.get_date()
print(datetime.strptime("2023-10-12", "%Y-%m-%d").date().month)

