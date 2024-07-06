from msfx.lib.db_back2.column import Column
from msfx.lib.db_back2.relation import Relation
from msfx.lib.db_back2.table import Table
from msfx.lib.db_back2.types import Types

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

rel = Relation()
rel.set_type("FULL")
rel.set_local_table(sales)
rel.set_foreign_table(articles)
rel.append_segment(
    sales.columns().get_by_alias("CARTICLE"),
    articles.columns().get_by_alias("CARTICLE")
)

print(rel)