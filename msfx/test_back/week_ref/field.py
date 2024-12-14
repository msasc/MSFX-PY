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

from table import Table
class Table: pass

class Field:
    def __init__(self, name: str):
        self.__name: str = name
        self.__table: Table = None

    def set_table(self, table: Table):
        self.__table = table

    def get_name_table(self):
        if self.__table is None:
            return self.__name
        return self.__table.get_name() + "." + self.__name
