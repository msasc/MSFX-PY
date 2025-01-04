#  Copyright (c) 2025 Miquel Sas.
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

from typing import Optional, Tuple

from msfx.lib.db import Value
from msfx.lib.db.md import ColumnList

class Record:
    def __init__(self, columns: ColumnList):
        self.__columns: ColumnList = columns
        self.__values: Optional[Tuple[Value, ...]] = None