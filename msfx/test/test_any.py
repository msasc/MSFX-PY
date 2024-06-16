from msfx.lib.db.column import Column
from msfx.lib.util.error import check_argument_type, check_argument_value
print(f"Key must be of type {int.__name__} or {str.__name__}")
print(f"Key must be of type {int} or {str} or {Column}")

try:
    check_argument_type("name", 0.6, (int,))
except Exception as e:
    print(e)

try:
    index = -1
    check_argument_value("index", index >= 0, -1, ">= 0")
except Exception as e:
    print(e)