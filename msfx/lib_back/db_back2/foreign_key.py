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

from msfx.lib_back.db_back2.table import TableLink
from msfx.lib_back import error_msg

class ForeignKey(TableLink):
    """ A foreign key of a table. """
    def __init__(self):
        super().__init__()
        self.__name = ""
        self.__persistent = False
        self.__delete_restriction = "RESTRICT"

    def get_name(self):
        return self.__name
    def set_name(self, name):
        self.__name = name if isinstance(name, str) else ""

    def is_persistent(self):
        return self.__persistent
    def set_persistent(self, persistent):
        self.__persistent = persistent if isinstance(persistent, bool) else False

    def get_delete_restriction(self):
        return self.__delete_restriction
    def set_delete_restriction(self, delete_restriction):
        if delete_restriction is None or not isinstance(delete_restriction, str):
            error = error_msg("type error", "alias", type(delete_restriction), (str,))
            raise TypeError(error)
        delete_restrictions = ("RESTRICT", "CASCADE", "SET NULL")
        if not delete_restriction in delete_restrictions:
            error = error_msg("value error", "delete_restriction", delete_restriction, delete_restrictions)
            raise ValueError(error)
        self.__delete_restriction = delete_restriction

    # noinspection PyDictCreation
    def to_dict(self):
        data = {}
        data["name"] = self.__name
        data["persistent"] = self.__persistent
        data["deleteRestriction"] = self.__delete_restriction
        data |= super().to_dict()
        return data
