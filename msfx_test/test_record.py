#  Copyright (c) 2023 Miquel Sas.
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

from msfx.db.data import Types, Field, Fields, Value, Record
from decimal import Decimal

f_CARTICLE = Field()
f_CARTICLE.set_name("CARTICLE")
f_CARTICLE.set_type(Types.STRING)
f_CARTICLE.set_length(40)
f_CARTICLE.set_primary_key(True)

f_QSALES = Field()
f_QSALES.set_name("QSALES")
f_QSALES.set_type(Types.DECIMAL)
f_QSALES.set_length(20)
f_QSALES.set_decimals(6)

f_CCOMPONENT = Field(f_CARTICLE)
f_CCOMPONENT.set_name("CCOMPONENT")

fields: Fields = Fields()
fields.append_field(f_CARTICLE)
fields.append_field(f_CCOMPONENT)
fields.append_field(f_QSALES)

values = [
    Value("A325400200"),
    Value("K325400200"),
    Value(Decimal("3.00"))
]

rec = Record(fields, values)
print(rec.get_field("CARTICLE"))
print(rec.get_value("CARTICLE"))
print(rec.get_value("QSALES"))
print(rec.get_primay_key())

rec.set_value("CARTICLE", Value("A000000000"))
print(rec.get_value("CARTICLE"))
print(Types.DECIMAL.is_numeric())

rec.set_value("CARTICLE", "A999999999")
print(rec.get_value("CARTICLE"))

rec.set_value("QSALES", 1.25)
print(rec.get_value("QSALES"))
print(len(rec))

indexes = [n for n in range(10)]
print(indexes)
print(rec)
