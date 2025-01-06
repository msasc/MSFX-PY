

def test_kwargs(**kwargs):
    if len(kwargs) == 0:
        print("No arguments passed")
        kwargs["name"] = False
    print(kwargs)

test_kwargs()