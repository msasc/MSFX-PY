#  Copyright (c) 2023 Miquel Sas.
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

from field import Field, FieldList
from value import Value

class Record:
    """
    A record packs a list of values and their corresponding field definitions, as well a list of flags
    indicating wheter the value in the record has been modified.
    """
    def __init__(self, fields: FieldList, values: list or None = None):
        """
        Creates a new record.
        :param fields: The definitions of fields.
        :param values: The list of values, if not passed the default values of the fields are used.
        """

        if fields is None or not isinstance(fields, FieldList):
            raise Exception("The list of fields is required.")

        self.__fields: FieldList = fields
        self.__values: list(Value)
        if values is None:
            self.__values = list(fields.get_default_values())
        else:
            if len(values) != len(fields):
                raise Exception("Invalid len values/fields must match")
            self.__values = list(values)
