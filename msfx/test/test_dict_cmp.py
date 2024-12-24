d1 = {}
d1["name"] = "John"
d1["age"] = 18
d1["gender"] = "male"
d1["props"] = {"care": "A lot", "why": "matter"}

d2 = {}
d2["name"] = "John"
d2["age"] = 18
d2["gender"] = "male"
d2["props"] = {"care": "A lot", "why": "matter"}

print(d1 == d2)
print(len(d1))

for k, v in d1.items():
    print(k, v)

