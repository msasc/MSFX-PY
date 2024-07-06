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
from msfx.lib.db_back.order import Order
from msfx.lib.dn import Schema, get_string, put_string

class Index(Order):
    """ An index definition. """

    NAME = "name"
    DESCRIPTION = "description"
    UNIQUE = "unique"
    TABLE = "table"
    SCHEMA = "schema"

    schema = Schema()
    schema.add(key=NAME, value_type=str, default_value="")

    def __init__(self, index=None):
        super(Index, self).__init__(index)

    def get_name(self): return get_string(self._data(), Index.NAME)
    def set_name(self, name: str): put_string(self._data(), Index.NAME, name)

    def __str__(self) -> str: return str(self._data())
    def __repr__(self): return self.__str__()
