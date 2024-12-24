from msfx.lib.vdict import get_bool

data = {}
data["one"] = "One"
data["two"] = "Two"
data["three"] = "Three"
data["four"] = "Four"
data["five"] = "Five"
data["six"] = "Six"
data["seven"] = "Seven"
data["eight"] = "Eight"
data["nine"] = "Nine"

try:
    print(get_bool(data, "one"))
except Exception as e:
    print(e)

master_keys = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]
required_keys = ["six", "seven", "eight", "nine", "ten", "eleven", "twelve"]

try:
    print("Hello")
    # validate_dict(data, master_keys, required_keys)
except Exception as e:
    print(e)
