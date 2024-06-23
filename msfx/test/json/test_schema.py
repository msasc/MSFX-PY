from decimal import Decimal

from msfx.lib.json import Schema


schema = Schema()
schema.add(key="name", value_type=str, default_value="")

tp = Decimal
print(tp())