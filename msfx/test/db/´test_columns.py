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
import json

from msfx.lib.db.meta import Column, Columns
from msfx.lib.db.types import Types

ccompany = Column()
ccompany.set_name("CCOMPANY")
ccompany.set_type(Types.STRING)
ccompany.set_length(30)

carticle = Column()
carticle.set_name("CARTICLE")
carticle.set_type(Types.STRING)
carticle.set_length(20)

qsales = Column()
qsales.set_name("QSALES")
qsales.set_type(Types.DECIMAL)
qsales.set_decimals(2)

qprod = Column()
qprod.set_name("QPROD")
qprod.set_type(Types.DECIMAL)
qprod.set_decimals(2)

columns = Columns()
columns.add_column(ccompany)
columns.add_column(carticle)
columns.add_column(qsales)
columns.add_column(qprod)

for column in columns:
    print(column)

print()

for i in range(len(columns)):
    print(columns[i])

print()
print(columns.get_columns())
print()
print(columns.get_column_by_alias("CARTICLE"))

columns.remove_column("CARTICLE")
print(columns.get_columns())
