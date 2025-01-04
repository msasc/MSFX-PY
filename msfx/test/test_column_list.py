from msfx.lib.db import Types
from msfx.lib.db.md import Column, ColumnList

carticle = Column()
carticle.set_name("CARTICLE")
carticle.set_type(Types.STRING)
carticle.set_length(20)
carticle.set_header("Article code")

qsales = Column()
qsales.set_name("QSALES")
qsales.set_type(Types.DECIMAL)
qsales.set_length(24)
qsales.set_scale(2)
qsales.set_header("Quantity")

cols = ColumnList()
cols.append(carticle)
cols.append(qsales)

print(cols.get_by_alias("CARTICLE"))
print(cols.get_by_alias("QSALES"))

cols_ro = cols.columns
print(cols_ro.get_by_alias("QSALES"))
# cols_ro.append(carticle)

print(len(cols))
