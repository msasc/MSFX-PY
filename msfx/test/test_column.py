from msfx.lib.db import Types
from msfx.lib.db.meta import Column

col = Column()
print(col.get_type())
col.set_name("QSALES")
col.set_type(Types.DECIMAL)
col.set_length(24)
col.set_scale(2)
col.set_header("Quantity")
print(col.get_type())

col.get_props().set_string("TURURUT", "SETZE HORES")
print(col.get_props().get_string("TURURUT"))

print(col)
