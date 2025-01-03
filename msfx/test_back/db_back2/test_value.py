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

from msfx.lib_back2.db_back2.types import Types
from msfx.lib_back2.db_back2.value import Value

val = Value(Types.DATE)
print(val)

print(Types.get_types_null())
val_decimal = Value(Decimal(2.45))
val_float = Value(2.45)
print(val_decimal == val_float)

val_date = Value(date.today())
print(val_decimal == val_date)
print(val_decimal.is_comparable(val_float))
