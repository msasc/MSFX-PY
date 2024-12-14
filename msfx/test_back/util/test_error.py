from msfx.lib_back import error_msg, check_type

error = error_msg("function error", "function", "EXP", ("MIN", "MAX", "AVG"))
print(error)

error = error_msg("type error", "name", type(10), (str,))
print(error)

error = error_msg("value error", "option", 10, (1, 2))
print(error)

print(type(None))