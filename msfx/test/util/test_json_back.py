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
from datetime import date
from decimal import Decimal

from msfx.lib.db_back.json_back import JSON

js1 = JSON()
js1.put_string(key="name", value="Miquel Sas")
js1.put_integer(key="age", value=66)
js1.put_date(key="born", value=date.fromisoformat("1958-05-08"))
js1.put_binary("bin", bytes([0, 4, 8, 16, 32, 64, 128, 255]))
js1.put_decimal("amount", Decimal("10.750"))

print(js1.dumps())

js2 = JSON()
js2.put_string(key="name", value="Joan Fabregat")
js2.put_integer(key="age", value=65)

js1.put_json("json", js2)

print(js1.dumps())

val_js = js1.get_json("json")
if isinstance(val_js, JSON):
    print(val_js.dumps())

x = js1.data().get("XX")
print(x)