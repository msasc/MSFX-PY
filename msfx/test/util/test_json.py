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
from datetime import datetime, date
from decimal import Decimal

from msfx.lib.util.json import JSON

json = JSON()
json.put_string(key="name", value="Miquel Sas")
json.put_int(key="age", value=66)
json.put_date(key="date born", value=date.fromisoformat("1958-05-08"))
json.put_binary("bin", bytes([0, 4, 8, 16, 32, 64, 128, 255]))
json.put_decimal("amount", Decimal("10.750"))

print(json.dumps())
print(str(json.get_date("date born")))
print(json.get_int("amount"))
print(json.get_float("amount"))
print(json.get_decimal("amount"))
print(json.get_binary("bin"))

print()

x = datetime.fromisoformat("1958-05-08T12:30:00")
print(str(x))
print(str(x.date()))
print(str(x.time()))


