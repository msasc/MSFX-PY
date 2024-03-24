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

from decimal import Decimal
from datetime import date, time, datetime

from msfx.lib.db.types import Types
from msfx.lib.db.json import JSON

def get_type(value: object) -> Types:
    """
    Check and return the type of the value.
    :param value: The value to check the type.
    :return: The type.
    :raises: TypeError if the type of the value is not a supported type.
    """
    if isinstance(value, bool): return Types.BOOLEAN
    if isinstance(value, Decimal): return Types.DECIMAL
    if isinstance(value, int): return Types.INTEGER
    if isinstance(value, float): return Types.FLOAT
    if isinstance(value, complex): return Types.COMPLEX
    if isinstance(value, date): return Types.DATE
    if isinstance(value, time): return Types.TIME
    if isinstance(value, datetime): return Types.DATETIME
    if isinstance(value, bytes): return Types.BINARY
    if isinstance(value, str): return Types.STRING
    if isinstance(value, JSON): return Types.JSON
    raise TypeError(f"Invalid type of value {value}")
