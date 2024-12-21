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
    put_bool, put_decimal, put_integer, put_float, put_complex,
    put_string, put_date, put_time, put_datetime, put_binary, put_list, put_dict, put_any
)

class Properties:
    """
    Encapsulates accesses to a dictionary validating the types of the values.
    """
    def __init__(self, props=None):
        self.__props = None
        if isinstance(props, dict): self.__props = copy.deepcopy(props)
        if isinstance(props, Properties): self.__props = copy.deepcopy(props.__props)
        if self.__props is None: self.__props = {}

    def get_bool(self, key, default=False) -> bool: return get_bool(self.__props, key, default)
    def get_integer(self, key, default=0) -> int: return get_integer(self.__props, key, default)
    def get_float(self, key, default=0.0) -> float: return get_float(self.__props, key, default)
    def get_decimal(self, key, default=Decimal(0)) -> Decimal: return get_decimal(self.__props, key, default)
    def get_complex(self, key, default=complex(0, 0)) -> complex: return get_complex(self.__props, key, default)
    def get_string(self, key, default="") -> str: return get_string(self.__props, key, default)
    def get_date(self, key, default=None) -> date: return get_date(self.__props, key, default)
    def get_time(self, key, default=None) -> time: return get_time(self.__props, key, default)
    def get_datetime(self, key, default=None) -> datetime: return get_datetime(self.__props, key, default)
    def get_binary(self, key, default=None) -> bytes or bytearray: return get_binary(self.__props, key, default)
    def get_list(self, key, default=None) -> list: return get_list(self.__props, key, default)
    def get_dict(self, key, default=None) -> dict: return get_dict(self.__props, key, default)

    def get_any(self, key, default=None) -> Any: return get_any(self.__props, key, default)
    def get_props(self, key, default=None) -> Any:
        value = self.__props.get(key, default)
        check_class_name(value, Properties)
        return value

    def put_bool(self, key, value: bool): put_bool(self.__props, key, value)
    def put_decimal(self, key, value): put_decimal(self.__props, key, value)
    def put_integer(self, key, value): put_integer(self.__props, key, value)
    def put_float(self, key, value): put_float(self.__props, key, value)
    def put_complex(self, key, value): put_complex(self.__props, key, value)
    def put_string(self, key, value): put_string(self.__props, key, value)
    def put_date(self, key, value): put_date(self.__props, key, value)
    def put_time(self, key, value): put_time(self.__props, key, value)
    def put_datetime(self, key, value): put_datetime(self.__props, key, value)
    def put_binary(self, key, value): put_binary(self.__props, key, value)
    def put_list(self, key, value): put_list(self.__props, key, value)
    def put_dict(self, key, value): put_dict(self.__props, key, value)
    def put_any(self, key, value): put_any(self.__props, key, value)

    def put_props(self, key, value):
        check_class_name(value, Properties)
        put_any(self.__props, key, value)

