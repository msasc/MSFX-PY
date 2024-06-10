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

from msfx.lib.db_back.types import Types
from msfx.lib.db_back.field import Field, FieldList

f1 = Field()
f1.set_name("CARTICLE")
f1.set_type(Types.STRING)
f1.set_length(40)

f2 = Field()
f2.set_name("DARTICLE")
f2.set_type(Types.STRING)
f2.set_length(80)

flist = FieldList()
flist.append_field(f1)
flist.append_field(f2)

for f in flist:
    print(f)

print()

for i in range(len(flist)):
    print(flist[i])

print()
print(flist[0])
print(flist[1])
