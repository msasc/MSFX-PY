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

from msfx.lib_back.db import STRING, DECIMAL
from msfx.lib_back.db_back.column import Column
from msfx.lib_back.db_back.index import Index

ccompany = Column(name="CCOMPANY", type=STRING, length=20, primary_key=True)
carticle = Column(name="CARTICLE", type=STRING, length=20, primary_key=True)
qsales = Column(name="QSALES", type=DECIMAL, length=24, decimals=2)

index = Index()
index.set_name("COMPANY_ARTS_PK")

index.append(ccompany)
index.append(carticle)

print(index)
