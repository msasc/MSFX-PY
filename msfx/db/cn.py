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
from msfx.db.data import Record, RecordIterator

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
        pass
    @abstractmethod
    def is_closed(self) -> bool:
        """
        Check whether the underlying connection is closed.
        :return: A boolean.
        """
        pass
    @abstractmethod
    def is_auto_commit(self) -> bool:
        """
        Check the auto-commit status flag.
        :return: A boolean.
        """
        pass
    @abstractmethod
    def set_auto_commit(self, auto_commit: bool):
        """
        Set the auto-commit flag.
        :param auto_commit: A boolean.
        """
        pass
    @abstractmethod
    def begin(self):
        """
        Start a new transaction which can be committed by .commit() method,
        or cancelled by .rollback() method.
        """
        pass
    @abstractmethod
    def commit(self):
        """
        Commit the transaction started with .begin().
        """
        pass
    @abstractmethod
    def rollback(self):
        """
        Rollback the transaction started with .begin().
        """
        pass
    @abstractmethod
    def iterator(self, select: str) -> RecordIterator:
        """
        Creates and returns a record iterator applying the select or similar query.
        If the select query does not internally return a list of table or view rows,
        it should raise an exception.

        If the database connection does not support several iterators within a single
        connection it should raise an exception.

        The iterator returned must contain the list of fields. Those fields must have this
        db module type, and a property, 'DB_TYPE', thar return s the underlying database
        field type as a string, as well as 'DB_LENGTH' and 'DB_DECIMALS'

        :param select: The select or similar query that internally returns a set of rows.
        :return: The record iterator.
        """
        pass
    @abstractmethod
    def execute(self, command: str) -> int:
        """
        Execute a database command, INSERT, UPDATE, DELETE, or any other DDL command
        like for instance ALTER TABLE.

        If the command is a SELECT query that internally returns a set of rows it should
        raise an exception.

        The command, specially for INSERT, UPDATE and DELETE, can be affected by the 'begin',
        'commit' and 'rollback' transaction methods.

        :param command: The database command.
        :return: The number of affected rows.
        """
        pass

class Adapter(ABC):
    """
    Database adapter to connect to a database instance.
    """
    def __init__(self, **params):
        """
        Instantiates the adapther passing at least the necessary connection parameter,
        normally user, passwor, host...
        :param params: Connection and optionally additional parameters.
        """
        self.__params = params
    @abstractmethod
    def get_connection(self) -> Connection:
        """
        Returns a new fresh connection.
        :return: The connection.
        """
        pass