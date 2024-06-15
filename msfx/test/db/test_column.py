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

from msfx.lib.db.column import Column
from msfx.lib.db.types import Types
from msfx.lib.util.json import loads, dumps

column_1 = Column()
column_1.set_name("CARTICLE")
column_1.set_type(Types.STRING)
column_1.set_length(20)
print(column_1)

column_2 = Column()
column_2.set_name("QSALES")
column_2.set_type(Types.DECIMAL)
column_2.set_decimals(2)
column_2.set_primary_key(True)
print(column_2)

column_3 = Column(name="CCOMPANY", type=Types.STRING, length=20, header="Company")
print(column_3)
