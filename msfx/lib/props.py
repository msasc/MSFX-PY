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
import copy
from datetime import date, time, datetime
from decimal import Decimal
from typing import Any

from msfx.lib import check_class_name
from msfx.lib.vdict import (
    get_bool, get_integer, get_float, get_decimal, get_complex,
    get_string, get_date, get_time, get_datetime, get_binary, get_list, get_dict, get_any,
    set_bool, set_decimal, set_integer, set_float, set_complex,
    set_string, set_date, set_time, set_datetime, set_binary,
    set_list, set_tuple, set_dict, set_any
)

class Properties:
    """
    Encapsulates accesses to a dictionary validating the types of the values.
    """
    def __init__(self):
        self.__props = {}

    def copy(self):
        props = Properties()
        props.__props = copy.deepcopy(self.__props)
        return props

    def get_bool(self, key, default=False) -> bool:
        return get_bool(self.__props, key, default)
    def get_integer(self, key, default=0) -> int:
        return get_integer(self.__props, key, default)
    def get_float(self, key, default=0.0) -> float:
        return get_float(self.__props, key, default)
    def get_decimal(self, key, default=Decimal(0)) -> Decimal:
        return get_decimal(self.__props, key, default)
    def get_complex(self, key, default=complex(0, 0)) -> complex:
        return get_complex(self.__props, key, default)
    def get_string(self, key, default="") -> str:
        return get_string(self.__props, key, default)
    def get_date(self, key, default=None) -> date:
        return get_date(self.__props, key, default)
    def get_time(self, key, default=None) -> time:
        return get_time(self.__props, key, default)
    def get_datetime(self, key, default=None) -> datetime:
        return get_datetime(self.__props, key, default)
    def get_binary(self, key, default=None) -> bytes or bytearray:
        return get_binary(self.__props, key, default)
    def get_list(self, key, default=None) -> list:
        return get_list(self.__props, key, default)
    def get_dict(self, key, default=None) -> dict:
        return get_dict(self.__props, key, default)

    def get_any(self, key, default=None) -> Any:
        return get_any(self.__props, key, default)
    def get_props(self, key, default=None) -> Any:
        value = self.__props.get(key, default)
        check_class_name(value, Properties)
        return value

    def set_bool(self, key, value: bool):
        set_bool(self.__props, key, value)
    def set_decimal(self, key, value):
        set_decimal(self.__props, key, value)
    def set_integer(self, key, value):
        set_integer(self.__props, key, value)
    def set_float(self, key, value):
        set_float(self.__props, key, value)
    def set_complex(self, key, value):
        set_complex(self.__props, key, value)
    def set_string(self, key, value):
        set_string(self.__props, key, value)
    def set_date(self, key, value):
        set_date(self.__props, key, value)
    def set_time(self, key, value):
        set_time(self.__props, key, value)
    def set_datetime(self, key, value):
        set_datetime(self.__props, key, value)
    def set_binary(self, key, value):
        set_binary(self.__props, key, value)
    def set_list(self, key, value):
        set_list(self.__props, key, value)
    def set_tuple(self, key, value):
        set_tuple(self.__props, key, value)
    def set_dict(self, key, value):
        set_dict(self.__props, key, value)
    def set_any(self, key, value):
        set_any(self.__props, key, value)

    def set_props(self, key, value):
        check_class_name(value, Properties)
        set_any(self.__props, key, value)

    def __iter__(self):
        return self.__props.__iter__()
    def __len__(self) -> int:
        return len(self.__props)
    def __eq__(self, other) -> bool:
        return self.__props == other.__props
    def __str__(self) -> str:
        return str(self.__props)
    def __repr__(self):
        return self.__str__()
