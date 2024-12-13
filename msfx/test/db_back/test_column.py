
from msfx.lib_back.db import STRING, DECIMAL
from msfx.lib_back.db_back.column import Column, ColumnList

ccompany = Column(name="CCOMPANY", type=STRING, length=20, primary_key=True)
carticle = Column(name="CARTICLE", type=STRING, length=20, primary_key=True)
qsales = Column(name="QSALES", type=DECIMAL, length=24, decimals=2)

columns = ColumnList()
columns.append(ccompany)
columns.append(carticle)
columns.append(qsales)

print(columns.get_by_alias("QSALES"))
print()
print(columns)

print(columns.default_values())
