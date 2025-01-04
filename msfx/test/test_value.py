from decimal import Decimal

from msfx.lib.db import Value


# bool
value = Value(False)
print(value)
value.set_bool(True)
print(value)

# Decimal
value = Value(Decimal("3.57"))
print(value)
print(value.get_scale())
value.set_float(3.637)
print(value)
print(value.get_float())

dec = Decimal(3.57)
print(float(dec))

b = bytes([72, 101, 108, 108, 111])
print(b.decode('utf-8'))
ba = bytearray(b)
print(ba.decode('utf-8'))
print(bytes(ba))
print(bytearray(bytes(ba)))


# value_date: Value = Value(datetime.now().date())
# value_time: Value = Value(datetime.now().time())
# value_string: Value = Value("Hello")
# value_decimal: Value = Value(Decimal("3.65"))
# print(value_date)
# print(value_time)
# print(value_string)
# print(value_decimal)
#
# scale = abs(int(value_decimal.get_decimal().as_tuple().exponent))
# print(scale)
