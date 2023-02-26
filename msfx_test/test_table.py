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

from msfx.db.data import Types, Field, Index, Table

f_CARTICLE = Field()
f_CARTICLE.set_name("CARTICLE")
f_CARTICLE.set_type(Types.STRING)
f_CARTICLE.set_length(40)
f_CARTICLE.set_persistent(True)
f_CARTICLE.set_primary_key(True)

f_QSALES = Field()
f_QSALES.set_name("QSALES")
f_QSALES.set_type(Types.DECIMAL)
f_QSALES.set_length(20)
f_QSALES.set_decimals(4)
f_QSALES.set_persistent(True)

f_CCOMPONENT = Field(f_CARTICLE)
f_CCOMPONENT.set_name("CCOMPONENT")

f_CCOMPANY = Field(f_CARTICLE)
f_CCOMPANY.set_name("CCOMPANY")

table = Table()
table.set_name("SALES")
table.set_schema("MARG")
table.append_field(f_CARTICLE)
table.append_field(f_CCOMPONENT)
table.append_field(f_QSALES)

index = Index()
index.append_segment(f_CARTICLE)
index.append_segment(f_CCOMPONENT)
index.append_segment(f_QSALES)
# index.append_segment(f_CCOMPANY)
table.append_index(index)

table.validate_and_setup()

print(table)
for index in table.get_indexes():
    print(index)

pk: Index = table.get_primary_key()
print(pk)

print(table.get_field("CARTICLE"))
print(table.get_field("CARTICLE").is_foreign())