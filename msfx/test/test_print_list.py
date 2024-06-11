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
class MyObject:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return f"MyObject(name={self.name}, value={self.value})"
    def __repr__(self):
        return self.__str__()

# Create a list of objects
objects = [MyObject('apple', 1), MyObject('banana', 2), MyObject('cherry', 3)]

# Print the list of objects
print(objects)
