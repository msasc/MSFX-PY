from msfx.lib_back import loads, dumps
from msfx.lib_back.db import STRING
from msfx.lib_back.db.column import Column, ColumnList

ccompany = Column(name="CCOMPANY", type=STRING, length=30, header="Company", primary_key=True)
carticle = Column(name="CARTICLE", type=STRING, length=30, header="Article")

columns = ColumnList()
columns.append(ccompany)
columns.append(carticle)

print(columns)
print(columns.to_string())

columns2 = ColumnList()
columns2.from_string(columns.to_string())
print(columns2.to_string())
