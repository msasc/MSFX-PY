from msfx.lib_back2 import check_type, check_value

try:
    check_type("code", str, (int, float))
except Exception as e:
    print(e)

try:
    check_value("code", 10 < 20, "<", ("=", ">="))
except Exception as e:
    print(e)
try:
    check_value("index", -1 < 0,"index < 0", (" index >= 0",))
except Exception as e:
    print(e)
