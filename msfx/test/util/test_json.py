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

from msfx.lib.util.json import put_string, put_integer, put_date, put_binary, put_decimal, dumps, put_dict

js1 = {}
put_string(dct=js1, key="name", value="Miquel Sas")
put_integer(dct=js1, key="age", value=66)
put_date(dct=js1, key="born", value=date.fromisoformat("1958-05-08"))
put_binary(dct=js1, key="bin", value=bytes([0, 4, 8, 16, 32, 64, 128, 255]))
put_decimal(dct=js1, key="amount", value=Decimal("10.750"))

print(dumps(js1))

js2 = {}
put_string(dct=js2, key="name", value="Joan Fabregat")
put_integer(dct=js2, key="age", value=65)

print(dumps(js2))

put_dict(dct=js1, key="dict", value=js2)
print(dumps(js1))
