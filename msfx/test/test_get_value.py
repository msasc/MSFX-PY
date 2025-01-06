import types
from datetime import date
from decimal import Decimal

from msfx.lib.db import get_value, Types

print(get_value(Types.DECIMAL, 4, Decimal(1.645)))
print(get_value(Types.DECIMAL, 4, 1.645))
print(get_value(Types.BOOLEAN, 4, True))
print(get_value(Types.STRING, 4, "tus huevos machote"))
print(get_value(Types.DATE, 4, date.today()))