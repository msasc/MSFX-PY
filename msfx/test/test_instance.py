from typing import Optional

def get_name(name):
    return name if isinstance(name, str) else "None"
    # return name if name else "None"

print(get_name(None))
print(get_name("Charles"))
print(get_name(10.0))