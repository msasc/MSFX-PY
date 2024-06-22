from typing import List

from msfx.lib.util.globals import dict_str
from msfx.lib.util.iterator import Iterator
from msfx.lib.util.json import dumps

data = {}
data["name"] = "Miquel"
data["age"] = 66
data["male"] = True
data["prefs"] = ["ONE", "TWO", "THREE", "FOUR"]

print(dict_str(data))

print(dumps(data, indent=3))

# lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# i = Iterator(data)
# while i.has_next():
#     print(i.next())
# i = Iterator(data["prefs"])
# while i.has_next():
#     print(i.next())
