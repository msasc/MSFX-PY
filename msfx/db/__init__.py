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

"""
msfx.db package enables Python programs to access SQL databases using an
interface detached from the underlying engine, be MariaDB, Postgresql,
Oracle or whatever has implemented an adapter.
"""

from decimal import Decimal, ROUND_HALF_UP

def is_numeric_value(value: object) -> bool:
    if (isinstance(value, Decimal) or
        isinstance(value, int) or
        isinstance(value, float) or
        isinstance(value, complex)):
        return True
    return False

def get_decimal(num: object, dec: int = 0) -> Decimal:
    if isinstance(num, complex):
        return Decimal(num.real).quantize(Decimal(10) ** -dec, rounding=ROUND_HALF_UP)
    if (isinstance(num, Decimal) or
        isinstance(num, int) or
        isinstance(num, float)):
        return Decimal(num).quantize(Decimal(10) ** -dec, rounding=ROUND_HALF_UP)
    raise TypeError(f"Invalid type for num {num}")

def get_integer(num: object) -> int:
    if isinstance(num, complex): return int(num.real)
    if (isinstance(num, Decimal) or
        isinstance(num, int) or
        isinstance(num, float)):
        return int(num)
    raise TypeError(f"Invalid type for num {num}")

def get_float(num: object) -> float:
    if isinstance(num, complex): return float(num.real)
    if (isinstance(num, Decimal) or
        isinstance(num, int) or
        isinstance(num, float)):
        return float(num)
    raise TypeError(f"Invalid type for num {num}")

def get_complex(num: object) -> complex:
    if (isinstance(num, Decimal) or
        isinstance(num, int) or
        isinstance(num, float) or
        isinstance(num, complex)):
        return complex(num)
    raise TypeError(f"Invalid type for num {num}")
