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

"""
Packs global utility functions on numbers, dates, times, strings.
If the number of functions increases too much, this file will be
splited into category files per subject.
"""
from _decimal import Decimal
from datetime import datetime
from importlib import import_module

def is_valid_datetime(datetime_string: str, datetime_format: str) -> bool:
    try:
        datetime.strptime(datetime_string, datetime_format)
        return True
    except ValueError:
        return False

def is_valid_iso_date(date_string: str) -> bool:
    if not isinstance(date_string, str):
        return False
    if len(date_string) != 10:
        return False
    return is_valid_datetime(date_string, "%Y-%m-%d")

def is_valid_iso_time(time_string: str) -> bool:
    if not isinstance(time_string, str):
        return False
    if len(time_string) < 8:
        return False
    if len(time_string) == 8:
        return is_valid_datetime(time_string, "%H:%M:%S")
    return is_valid_datetime(time_string, "%H:%M:%S.%f")

def is_valid_iso_datetime(datetime_string: str) -> bool:
    if not isinstance(datetime_string, str):
        return False
    if len(datetime_string) < 19:
        return False
    datetime_string = datetime_string.replace(" ", "T")
    if len(datetime_string) == 19:
        return is_valid_datetime(datetime_string, "%Y-%m-%dT%H:%M:%S")
    return is_valid_datetime(datetime_string, "%Y-%m-%dT%H:%M:%S.%f")

def is_valid_hex_string(hex_string: str) -> bool:
    try:
        bytes.fromhex(hex_string)
        return True
    except ValueError:
        return False

def is_valid_integer(string: str) -> bool:
    if not isinstance(string, str):
        return False
    try:
        int(string)
        return True
    except ValueError:
        return False

def is_valid_float(string: str) -> bool:
    if not isinstance(string, str):
        return False
    try:
        float(string)
        return True
    except ValueError:
        return False

def is_valid_decimal(string: str) -> bool:
    if not isinstance(string, str):
        return False
    try:
        Decimal(string)
        return True
    except ValueError:
        return False

def is_numeric(value) -> bool:
    return isinstance(value, (int, float, Decimal, complex))

def list_get(lst, index, default=None):
    try: return lst[index]
    except IndexError: return default

def error_msg(msg: str, arg: str, val: object, exp: (object,)):
    err = "argument '" + arg + "' " + msg + ", expected "
    if len(exp) == 1:
        err += "'" + str(exp[0]) + "'"
    else:
        err += "one of ("
        for i in range(len(exp)):
            if i > 0: err += ", "
            err += "'" + str(exp[i]) + "'"
        err += ")"
    err += ", got '" + str(val) + "'"
    return err

def value_str(v: object, indent=0) -> str:
    s = ""
    if isinstance(v, str):
        s += "'" + v + "'"
    if isinstance(v, (int, float, complex, Decimal, bool)):
        s += str(v)
    if isinstance(v, (list, tuple)):
        s += list_str(v)
    if isinstance(v, dict):
        s += dict_str(v)
    return s

def item_str(item: (str, object), indent= 0):
    k, v = item
    s = "'" + k + "': "
    s += value_str(v)
    return s

def list_str(lst: (list, tuple), indent= 0) -> str:
    comma = False
    s = "["
    for v in lst:
        if comma: s += ", "
        s += value_str(v, indent)
        comma = True
    s += "]"
    return s

def dict_str(data: dict, indent=0) -> str:
    comma = False
    s = "{"
    for item in data.items():
        if comma: s += ", "
        s += item_str(item, indent)
        comma = True
    s += "}"
    return s

def full_class_name(clazz):
    return f"{clazz.__module__}.{clazz.__qualname__}"

def instantiate(full_class_name, *args, **kwargs):
    # Split the full class name into module path and class name
    module_path, class_name = full_class_name.rsplit('.', 1)

    # Dynamically import the module
    module = import_module(module_path)

    # Retrieve the class from the module
    cls = getattr(module, class_name)

    # Instantiate the class
    instance = cls(*args, **kwargs)

    return instance
