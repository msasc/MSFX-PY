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

from decimal import Decimal, ROUND_HALF_UP
from functools import wraps

def check_class_name(arg, clazz):
    if arg is None: return
    arg_class = arg.__module__ + '.' + arg.__class__.__name__
    chk_class = clazz.__module__ + '.' + clazz.__name__
    if arg_class != chk_class: raise TypeError("{} expected to be {}".format(arg_class, chk_class))

def round_num(value: (Decimal, float, int, complex), scale: int) -> Decimal:
    if isinstance(value, complex):
        value = value.real
    return Decimal(value).quantize(Decimal(f"1e-{scale}"), rounding=ROUND_HALF_UP)

def check_numeric(value: (Decimal, float, int)):
    if not isinstance(value, (Decimal, float, int)):
        raise TypeError("{} expected to be one of Decimal, float, int".format(value))


class MutableDecimal:
    """ A mutable decimal or in general number."""
    def __init__(self, value: (Decimal, float, int) = None, scale: int = -1):
        """
        Initializes this mutable decimal. If the value is None, the value is zero.
        If the scale is GE zero, then it is preserved in all operations.
        :param value:
        :param scale:
        """
        if value: check_numeric(value)
        self.__value = Decimal(0) if value is None else Decimal(value)
        self.__scale = scale
        self.__preserve_scale__()

    def __preserve_scale__(self):
        if self.__scale >= 0:
            self.__value = round_num(self.__value, self.__scale)

    def get(self) -> Decimal:
        return self.__value

    def set(self, value: (Decimal, float, int)):
        check_numeric(value)
        self.__value = Decimal(value)
        self.__preserve_scale__()

    def add(self, value: (Decimal, float, int)):
        check_numeric(value)
        self.__value += Decimal(value)
        self.__preserve_scale__()

    def substract(self, value: (Decimal, float, int)):
        check_numeric(value)
        self.__value -= Decimal(value)
        self.__preserve_scale__()

    def multiply(self, value: (Decimal, float, int)):
        check_numeric(value)
        self.__value *= Decimal(value)
        self.__preserve_scale__()

    def divide(self, value: (Decimal, float, int)):
        check_numeric(value)
        self.__value /= Decimal(value)
        self.__preserve_scale__()

    def __str__(self) -> str: return str(self.__value)
    def __repr__(self): return self.__str__()
