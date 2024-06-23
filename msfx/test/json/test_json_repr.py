from decimal import Decimal

from msfx.lib.json import JSON

obj = JSON()
obj.put_integer("-integer-", 235)
obj.put_float("-float-", 235.43)
obj.put_decimal("-decimal-", Decimal("1.345"))
obj.put_complex( "-complex-", complex(3.45, 7.23))

print(obj.to_dict())
print(obj.to_string())
#
# copy = msfx.lib.json_back.loads(msfx.lib.json_back.dumps(data))
# print(copy)
# print(msfx.lib.json_back.dumps(copy))
#
# data["error"] = Column()
# msfx.lib.json_back.validate_dict(data)
