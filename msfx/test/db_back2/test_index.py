from msfx.lib_back.db_back2.column import Column
from msfx.lib_back.db_back2.index import Index
from msfx.lib_back.db_back2.table import Table
from msfx.lib_back.db_back2.types import Types

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