from msfx.lib import loads
from msfx.lib.db import STRING
from msfx.lib.db.column import Column, ColumnList

ccompany = Column(name="CCOMPANY", type=STRING, length=30, header="Company", primary_key=True)
carticle = Column(name="CARTICLE", type=STRING, length=30, header="Article")
print(ccompany.to_string())
print(carticle.to_string())

ccompany_chk = Column()
ccompany_chk.from_string(ccompany.to_string())
print(ccompany_chk.to_string())
print()

cols = ColumnList()
cols.append(ccompany)
cols.append(carticle)
print(cols)
print(cols.to_string())
print(loads(cols.to_string()))

# cols2 = ColumnList()
# cols2.from_string(cols.to_string())
# print(cols2)
# print(len(cols2))
# print(cols2.get_by_index(0))