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

from msfx.lib.db.column import Column, ColumnList
from msfx.lib.db.types import Types

column_1 = Column(name="CCOMPANY", type=Types.STRING, length=20, primary_key=True, header="Company")
print(column_1)

column_2 = Column()
column_2.set_name("CARTICLE")
column_2.set_type(Types.STRING)
column_2.set_length(20)
column_2.set_primary_key(True)
print(column_2)

column_3 = Column()
column_3.set_name("QSALES")
column_3.set_type(Types.DECIMAL)
column_3.set_decimals(2)
print(column_3)

column_list = ColumnList()
column_list.append(column_2)
column_list.append(column_3)
column_list.append(column_1)
print(column_list)

print(column_list.get_by_alias("CARTICLE"))