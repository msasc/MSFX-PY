
from msfx.lib.db import STRING, DECIMAL
from msfx.lib.db.column import Column, ColumnList
from msfx.lib.dn import dumps

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

cols_data = dumps(columns.to_dict())
cols2 = ColumnList(cols_data)
print(cols2)

print(columns.default_values())
