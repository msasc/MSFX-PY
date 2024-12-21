from msfx.lib_back2.db import STRING, DECIMAL
from msfx.lib_back2.db.column import Column, ColumnList
from msfx.lib_back2.db.order import Order

ccompany = Column(name="CCOMPANY", type=STRING, length=30, header="Company", primary_key=True)
carticle = Column(name="CARTICLE", type=STRING, length=30, header="Article", primary_key=True)
qsales = Column(name="QSALES", type=DECIMAL, length=24, decimals=2, header="QSales")

ord = Order()
ord.append(ccompany)
ord.append(carticle)
print(ord)

ord2 = Order()
ord2.from_string(ord.to_string())

print(ord2)