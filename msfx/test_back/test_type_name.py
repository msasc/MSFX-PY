from msfx.lib_back2 import Data, register_class, check_type
from msfx.lib_back2.db.column import Column

class TableClass(Data):
    def from_dict(self, data: dict):
        pass

print(TableClass.__name__)

check_type("arg", "Hello", (str,))
# check_type("arg", 10, (str,))

table = TableClass()

print(isinstance(TableClass, Data))
print(issubclass(TableClass, Data))

register_class("table_class", TableClass)
register_class("table_class", Column)