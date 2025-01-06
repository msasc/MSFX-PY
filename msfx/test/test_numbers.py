from decimal import Decimal

from msfx.lib import round_num

dec1 = Decimal("3.55")
dec2 = Decimal("3.25")

print(dec1 * dec2)
print(dec1 / dec2)
print(dec1 // dec2)
print(dec1 / Decimal(1.00658))
print(dec1 / 2)
print(type(round(dec1,1)))