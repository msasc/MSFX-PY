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

""" Connection utilities """

from abc import ABC, abstractmethod

class Cursor: pass

class Connection(ABC):
    """
    A simplified connection to an underlying SQL database.
    """
    @abstractmethod
    def close(self):
        """
        Close the underlying connection.
        """
    @abstractmethod
    def is_closed(self) -> bool:
        """
        Check whether the underlying connection is closed.
        :return: A boolean.
        """
    @abstractmethod
    def is_auto_commit(self) -> bool:
        """
        Check the auto-commit status flag.
        :return: A boolean.
        """
    @abstractmethod
    def set_auto_commit(self, auto_commit: bool):
        """
        Set the auto-commit flag.
        :param auto_commit: A boolean.
        """
    @abstractmethod
    def begin(self):
        """
        Start a new transaction which can be committed by .commit() method,
        or cancelled by .rollback() method.
        """
    @abstractmethod
    def commit(self):
        """
        Commit the transaction started with .begin().
        """
    @abstractmethod
    def rollback(self):
        """
        Rollback the transaction started with .begin().
        """
    @abstractmethod
    def cursor(self, **kwargs) -> Cursor:
        """
        Create and return a cursor.
        :param kwargs: Arguments, normally database dependent.
        :return: A cursor object.
        """

class Cursor(ABC):
    @abstractmethod
    def close(self):
        """
        Close the underlying connection.
        """
    @abstractmethod
    def is_closed(self) -> bool:
        """
        Check whether the underlying connection is closed.
        :return: A boolean.
        """