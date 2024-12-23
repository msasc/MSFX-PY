from msfx.lib.db import OrderKey, Value
k1 = []
k1.append((10, True))
k1.append((20, True))
k1.append(("John", False))

k2 = []
k2.append((10, True))
k2.append((20, True))
k2.append(("John", False))

print(k1 == k2)

ok1 = OrderKey()
ok1.append(Value(10), True)
ok1.append(Value(20), True)
ok1.append(Value("John"), False)

ok2 = OrderKey()
ok2.append(Value(10), True)
ok2.append(Value(20), True)
ok2.append(Value("John"), False)

print(ok1 == ok2)
