#  Copyright (c) 2024 Miquel Sas.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

def params_positional(a, b):
    print(a)
    print(b)

def params_var_lenght(*args):
    for arg in args:
        print(arg)

def params_kwargs(**kwargs):
    for key, value in kwargs.items():
        print(f"key: {key}, value: {value}")
    print(kwargs["name"])
    print(kwargs.__contains__("name"))

if __name__ == "__main__":
    params_positional(b="World", a="Hello")
    params_var_lenght("Mucho", "mas")
    params_kwargs(name="John", age=10)