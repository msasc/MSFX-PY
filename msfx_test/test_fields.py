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

from msfx.db.data import Types, Field, Fields

f_CARTICLE = Field()
f_CARTICLE = Field()
f_CARTICLE.set_name("CARTICLE")
f_CARTICLE.set_type(Types.STRING)
f_CARTICLE.set_length(40)

f_QSALES = Field()
f_QSALES.set_name("QSALES")
f_QSALES.set_type(Types.DECIMAL)
f_QSALES.set_length(20)
f_QSALES.set_decimals(4)

f_CCOMPONENT = Field(f_CARTICLE)
f_CCOMPONENT.set_name("CCOMPONENT")

fields: Fields = Fields()
fields.append_field(f_CARTICLE)
fields.append_field(f_CCOMPONENT)
fields.append_field(f_QSALES)

print(fields.fields()[0])
print(fields.keys())
print(fields.get_field(0))
print(fields.get_field("CARTICLE"))
print(fields.get_field(1))
print(fields.get_field("CCOMPONENT"))

f_CARTDEST= Field(f_CARTICLE)
f_CARTDEST.set_name("CARTDEST")
print(fields.contains(f_CARTDEST))
