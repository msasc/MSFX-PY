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
Utilities to help manage concurrency.
"""

from threading import RLock
from typing import Generic, TypeVar

T = TypeVar('T')

class Atomic(Generic[T]):
    """
    Generic atomic reference wit get, set and get_and_set methods.
    """
    def __init__(self, value: T):
        self.__lock = RLock()
        self.__value = value

    def get(self) -> T:
        with self.__lock:
            return self.__value

    def set(self, value: T):
        with self.__lock:
            self.__value = value

    def get_and_set(self, value: T):
        with self.__lock:
            prev_value = self.__value
            self.__value = value
            return prev_value
