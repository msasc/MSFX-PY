from msfx.lib import get_bool, put_bool

data = {}
data["K"] = True
print(data)

try:
    print(get_bool(data, "K"))
except Exception as e:
    print(e)
else:
    print("No exc")

try:
    put_bool(data, "F", "ERRR")
except Exception as e:
    print(e)
else:
    print("No exc")

