from decimal import Decimal

from msfx.lib.db_back.column import Column
print(int())
print(float())
print(complex())
print(Decimal())

full_path_name = f"{Column.__module__}.{Column.__qualname__}"
print(full_path_name)

def name(clazz):
    return f"{clazz.__module__}.{clazz.__qualname__}"

print(name(Column))