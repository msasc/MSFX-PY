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

import json

class JSON:
    def __init__(self, json_data=None):
        """ Creates a JSON object dumping json string data. """
        self.__data: dict = {}
        if json_data is not None:
            self.loads(json_data)
    def loads(self, json_data):
        """ Loads the argument json_data string and merges it with this JSON internal dictionary data. """
        self.__data |= json.loads(json_data)
    def dumps(self) -> str:
        """ Dumps the internal dictionary data and returns a json string representation. """
        return json.dumps(self.__data)
    def merge(self, data: dict):
        """ Merges the argument dictionary data with this JSON internal dictionary data. """
        if type(data) is not dict: raise "Data to merge must be of dict type"
        self.__data |= data
    def data(self) -> dict:
        """ Gives access to the internal Python data dictionary. """
        return self.__data

    def __str__(self) -> str: return str(self.__data)
    def __eq__(self, other: object) -> bool:
        if isinstance(other, JSON): return self.__data == other.__data
        if isinstance(other, dict): return self.__data == other
        return super().__eq__(other)
