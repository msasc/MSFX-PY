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

class Field: pass

class Table:
    def __init__(self, name: str):
        self.__name: str = name
        self.__fields: list = []

    def add_field(self, field: Field):
        field.set_table(self)
        self.__fields.append(field)

    def fields(self) -> list:
        return self.__fields

    def get_name(self):
        return self.__name