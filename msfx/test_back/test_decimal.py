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
from decimal import Decimal, ROUND_HALF_UP
from types import NoneType

dec = Decimal("3.14159265").quantize(Decimal("0.000"), rounding=ROUND_HALF_UP)
print(dec)
dec = Decimal(0).quantize(Decimal("0.000"), rounding=ROUND_HALF_UP)
print(dec)

dec = Decimal("3.1459265")

k = 3.458768
print(round(k, 2))

dec = round(dec, 2)
print(type(dec))
print(round(dec, 2))
print(round(Decimal(), 4))
print(bool())
print(NoneType())
