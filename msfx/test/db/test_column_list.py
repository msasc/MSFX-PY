from msfx.lib.db.column import Column
from msfx.lib.db.column_list import ColumnList
from msfx.lib.db.types import Types
from msfx.lib.db.value import Value

column_1 = Column(name="CCOMPANY", type=Types.STRING, length=20, header="Company")
column_2 = Column(name="CARTICLE", type=Types.STRING, length=20, header="Article")
column_3 = Column(name="QSALES", type=Types.DECIMAL, decimals=2, header="Article")

column_list = ColumnList()
column_list.append_column(column_1)
column_list.append_column(column_2)
column_list.append_column(column_3)

print(column_1)
print(column_list)

value = Value("CCOMPANY")
print(value)
values = [Value("CCOMPANY"), Value("CARTICLE"), Value("QSALES")]
print(values)