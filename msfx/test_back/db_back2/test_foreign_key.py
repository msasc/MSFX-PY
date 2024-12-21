from msfx.lib_back2.db_back2.column import Column
from msfx.lib_back2.db_back2.foreign_key import ForeignKey
from msfx.lib_back2.db_back2.table import Table
from msfx.lib_back2.db_back2.types import Types

ccompany = Column(name="CCOMPANY", type=Types.STRING, length=30, primary_key=True)
carticle = Column(name="CARTICLE", type=Types.STRING, length=20, primary_key=True)
darticle = Column(name="DARTICLE", type=Types.STRING, length=80)
qsales = Column(name="QSALES", type=Types.DECIMAL, decimals=2)

sales = Table()
sales.set_name("SALES")
sales.columns().append(ccompany)
sales.columns().append(carticle)
sales.columns().append(qsales)

articles = Table()
articles.set_name("ARTICLES")
articles.columns().append(carticle)
articles.columns().append(darticle)

fk = ForeignKey()
fk.set_name("SALES_FK0")
fk.set_persistent(True)
fk.set_delete_restriction("CASCADE")
fk.set_local_table(sales)
fk.set_foreign_table(articles)
fk.append_segment(
    sales.columns().get_by_alias("CARTICLE"),
    articles.columns().get_by_alias("CARTICLE")
)

print(fk)
print(articles)