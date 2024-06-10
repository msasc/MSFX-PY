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

from datetime import date, time, datetime
from decimal import Decimal

from enum import Enum, EnumMeta

class Types(Enum, metaclass=EnumMeta):
    """	Supported types. """

    BOOLEAN = 0
    DECIMAL = 10
    INTEGER = 11
    FLOAT = 13
    COMPLEX = 14
    DATE = 20
    TIME = 21
    DATETIME = 22
    BINARY = 30
    STRING = 40
    LIST = 50
    DICTIONARY = 60

    @staticmethod
    def get_type(value: object):
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
        if isinstance(value, (tuple, list)): return Types.LIST
        if isinstance(value, dict): return Types.DICTIONARY
        raise TypeError(f"Invalid type of value {value}")

    @staticmethod
    def get_types_null() -> tuple:
        return Types.DATE, Types.TIME, Types.DATETIME, Types.BINARY

    @staticmethod
    def get_types_numeric() -> tuple:
        return Types.INTEGER, Types.FLOAT, Types.COMPLEX, Types.DECIMAL

    @staticmethod
    def get_types_length() -> tuple:
        return Types.DECIMAL, Types.STRING, Types.BINARY

