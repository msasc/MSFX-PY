from msfx.lib.db.column import Column
from msfx.lib.db.table import Table, TableLink
from msfx.lib.db.types import Types

ccompany = Column(name="CCOMPANY", type=Types.STRING, length=30, primary_key=True)
carticle = Column(name="CARTICLE", type=Types.STRING, length=20, primary_key=True)
darticle = Column(name="DARTICLE", type=Types.STRING, length=80)
qsales = Column(name="QSALES", type=Types.DECIMAL, decimals=2)


sales = Table()
sales.set_name("SALES")
sales.append_column(ccompany)
sales.append_column(carticle)
sales.append_column(qsales)

articles = Table()
articles.set_name("ARTICLES")
articles.append_column(carticle)
articles.append_column(darticle)

table_lnk = TableLink()
table_lnk.set_local_table(sales)
table_lnk.set_foreign_table(articles)
table_lnk.append_segment(
    sales.get_column_by_alias("CARTICLE"),
    articles.get_column_by_alias("CARTICLE")
)

print(table_lnk)