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

""" Global error functions. """
from typing import Any

def check_argument_type_name(argument: str, value: Any, valid_type_names):
    """ Checks if the argument with the given type_received is valid within the valid_type_names list. """
    if not isinstance(valid_type_names, tuple):
        raise TypeError("Valid type must be a tuple of type names")
    if not type(value).__name__ in valid_type_names:
        error = f"'{argument}' argument type name, expected "
        for i in range(len(valid_type_names)):
            if i > 0: error += " or "
            error += f"{valid_type_names[i]}"
        error += f", got {type(value).__name}"
        raise TypeError(error)

def check_argument_type(argument: str, value: Any, valid_types):
    """ Checks if the argument with the given type_received is valid"""
    if not isinstance(valid_types, tuple):
        raise TypeError("Valid type must be a tuple of types")
    if not isinstance(value, valid_types):
        error = f"'{argument}' argument type, expected "
        for i in range(len(valid_types)):
            if i > 0: error += " or "
            error += f"{valid_types[i]}"
        error += f", got {type(value)}"
        raise TypeError(error)

def check_argument_value(argument: str, condition: bool, value: object, expected: (object,)):
    """ Checks if the argument value """
    check_argument_type('argument', argument, (str,))
    check_argument_type('condition', condition, (bool,))
    check_argument_type('expected', expected, (object,))
    if not condition:
        error = "'" + argument + "' value error, expected one of ("
        for i in range(len(expected)):
            if i > 0: error += ", "
            error += "'" + str(expected[i]) + "'"
        error += "), got '" + str(value) + "'"
        raise ValueError(error)
