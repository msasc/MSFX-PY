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

from enum import Enum, EnumMeta, auto

class Types(Enum, metaclass=EnumMeta):
    """	Supported types mapped to the underlying SQL databases. """

    BOOLEAN = auto()
    """ Boolen value. """

    DECIMAL = auto()
    """ A numeric value with fixed number of decimal places. """
    INTEGER = auto()
    """ A numeric integer or long value. """
    FLOAT = auto()
    """ A numeric double (float) value. """
    COMPLEX = auto()
    """ A numeric complex value. """

    DATE = auto()
    """ A date value with ISO format '2022-12-21' """
    TIME = auto()
    """ A time value with ISO format '10:25:05.135000000' """
    DATETIME = auto()
    """ A date-time value with ISO format '2022-12-21T10:25:05.135000000' """

    BINARY = auto()
    """
    A binary value, stored in the underlying database in fields of types
    for instance TINYBLOB, BLOB, MEDIUMBLOB or LONGBLOB depending on the length.
    """

    STRING = auto()
    """
    A string value, stored in the underlying database in fields of types
    for instance VARCHAR, TINYTEXT, TEXT, MEDIUMTEXT or LONGTEXT depending on the length. 
    """

    JSON = auto()
    """
    A JSON object value, stored in the underlying database as a STRING.
    """

TYPES_NULL = (Types.DATE, Types.TIME, Types.DATETIME, Types.BINARY)
TYPES_LENGTH = (Types.DECIMAL, Types.STRING, Types.BINARY)