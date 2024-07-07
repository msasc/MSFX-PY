from msfx.lib.db import STRING, DECIMAL
from msfx.lib.db.column import Column, ColumnList
from msfx.lib.db.order import Order

ccompany = Column(name="CCOMPANY", type=STRING, length=30, header="Company", primary_key=True)
carticle = Column(name="CARTICLE", type=STRING, length=30, header="Article", primary_key=True)
qsales = Column(name="QSALES", type=DECIMAL, length=24, decimals=2, header="QSales")

order = Order()
order.append(ccompany)
order.append(carticle)
print(order)