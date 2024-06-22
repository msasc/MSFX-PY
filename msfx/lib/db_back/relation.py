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
from msfx.lib.db_back.table import TableLink
from msfx.lib.util.globals import error_msg

class Relation(TableLink):
    """ a Relation between two tables. """
    def __init__(self):
        super().__init__()
        self.__relation_type = "LEFT"

    def get_type(self):
        return self.__relation_type
    def set_type(self, relation_type):
        if relation_type is None or not isinstance(relation_type, str):
            error = error_msg("type error", "relation_type", type(relation_type), (str,))
            raise TypeError(error)
        relation_types = ("INNER", "LEFT", "RIGHT", "FULL", "CROSS")
        if not relation_type in relation_types:
            error = error_msg("value error", "relation_type", relation_type, relation_types)
            raise ValueError(error)
        self.__relation_type = relation_type

    # noinspection PyDictCreation
    def to_dict(self):
        data = {}
        data["relation_type"] = self.__relation_type
        data |= super().to_dict()
        return data
