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
from msfx.lib.db.meta import Column
from msfx.lib.db.types import Types

c1 = Column()
c1.set_name("CARTICLE")
c1.set_type(Types.STRING)
c1.set_length(20)

print(c1.get_name())
print(c1.get_type())

f2 = Column()
f2.set_name("QSALES")
f2.set_type(Types.DECIMAL)
f2.set_decimals(2)

v2 = f2.get_default_value()
print(f2.get_name())
print(f2.get_type())
print(v2)

f3 = Column()
f3.set_name("LIST")
f3.set_type(Types.LIST)
v3 = f3.get_default_value()
print(v3)
