
from msfx.lib.db_back2.column import Column
from msfx.lib.db_back2.order import Order
from msfx.lib.db_back2.types import Types

order = Order()

ccompany = Column()
ccompany.set_name("CCOMPANY")
ccompany.set_type(Types.STRING)
ccompany.set_length(30)

carticle = Column()
carticle.set_name("CARTICLE")
carticle.set_type(Types.STRING)
carticle.set_length(20)

order.append(ccompany)
order.append(carticle)

print(order)

print()
for c, b in order:
    print(f"{c}, {b}")
