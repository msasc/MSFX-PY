from msfx.lib.props import Properties

p1 = Properties()
p1.set_string("name", "John")
p1.set_integer("age", 35)

p2 = Properties()
p2.set_string("name", "John")
p2.set_integer("age", 36)

print(p1)
print(p1 == p2)