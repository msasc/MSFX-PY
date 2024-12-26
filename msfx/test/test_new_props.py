from types import SimpleNamespace

class Empty: pass

e = Empty()
print(e)

e.age = 20
e.name = "John"
print(e.age)
print(e.name)

k = SimpleNamespace()
k.age = 50

print(e.age)
print(k.age)