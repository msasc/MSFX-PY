from msfx.lib.db.column import Column
from msfx.lib.db.index import Index
from msfx.lib.db.table import Table
from msfx.lib.db.types import Types

ccompany = Column(name="CCOMPANY", type=Types.STRING, length=30)
carticle = Column(name="CARTICLE", type=Types.STRING, length=20)

table_sales = Table()
table_sales.set_name("SALES")
table_sales.columns().append(ccompany)
table_sales.columns().append(carticle)

pk = Index()
pk.set_name("SALES_PK")
pk.set_table(table_sales)
pk.append(ccompany)
pk.append(carticle)
pk.set_unique(True)

print(pk)