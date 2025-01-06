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

""" Defines an simple interface that SQL databases connectors must implement. """

from abc import ABC, abstractmethod
from datetime import date, time, datetime
from decimal import Decimal
from typing import Callable, Optional

from msfx.lib.db import Types, Value
from msfx.lib.db.md import Column, ColumnList
from msfx.lib.db.rs import Record


class DBAdapter(ABC):
    @abstractmethod
    def get_current_date(self) -> str:
        """ Returns the database current date as a string. """
        pass
    @abstractmethod
    def get_current_time(self, prec: int) -> str:
        """ Returns the database current time as a string. """
        pass
    @abstractmethod
    def get_current_datetime(self, prec: int) -> str:
        """ Returns the database current datetime as a string. """
        pass

    @abstractmethod
    def get_column_from_cursor_descr(self, descr: tuple) -> Column:
        """ Returns the database column from the given cursor tuple description. """
        pass
    @abstractmethod
    def get_column_db_def(self, column: Column) -> str:
        """ Returns the database column definition as a string. """
        pass
    @abstractmethod
    def get_lib_type(self, db_type: str) -> Types:
        """ Returns this library type given the database column type. """
        pass

    @abstractmethod
    def to_sql_date(self, value: date) -> str:
        """ Returns the SQL string of a date properly quoted. """
        pass
    @abstractmethod
    def to_sql_time(self, value: time) -> str:
        """ Returns the SQL string of a time properly quoted. """
        pass
    @abstractmethod
    def to_sql_datetime(self, value: datetime) -> str:
        """ Returns the SQL string of a date-time properly quoted. """
        pass
    @abstractmethod
    def to_sql_binary(self, value: (bytes, bytearray)) -> str:
        """ Returns the SQL string of a binary properly quoted. """
        pass

    def to_sql(self, value) -> str:
        """ Returns the SQL string of a value properly quoted. """
        if value is None:
            return "NULL"
        if isinstance(value, bool):
            return "Y" if value else "N"
        if isinstance(value, date):
            return self.to_sql_date(value)
        if isinstance(value, time):
            return self.to_sql_time(value)
        if isinstance(value, datetime):
            return self.to_sql_datetime(value)
        if isinstance(value, (Decimal, float, int, complex)):
            return str(value)
        if isinstance(value, (bytes, bytearray)):
            return self.to_sql_binary(value)
        if isinstance(value, str):
            return "'" + value + "'"
        if isinstance(value, Value):
            if value.is_none(): return "NULL"
            if value.is_boolean(): return "Y" if value.get_boolean() else "N"
            if value.is_decimal(): return str(value.get_decimal())
            if value.is_float(): return str(value.get_float())
            if value.is_integer(): return str(value.get_integer())
            if value.is_complex(): return str(value.get_complex())
            if value.is_date(): return self.to_sql_date(value.get_date())
            if value.is_time(): return self.to_sql_time(value.get_time())
            if value.is_datetime(): return self.to_sql_datetime(value.get_datetime())
            if value.is_binary(): return self.to_sql_binary(value.get_binary())
            if value.is_string(): return "'" + value.get_string() + "'"
        raise TypeError(f"Unsupported value: " + str(value))
    """ End class DBAdapter """
class DBCursor(ABC):
    @abstractmethod
    def get_adapter(self) -> DBAdapter: pass
    @abstractmethod
    def execute(self, operation, **parameters): pass
    @abstractmethod
    def fetchone(self) -> object: pass
    @abstractmethod
    def fetchall(self) -> object: pass
    @abstractmethod
    def fetchmany(self, size=100) -> object: pass
    @abstractmethod
    def count(self) -> int: pass
    @property
    @abstractmethod
    def description(self): pass
    @property
    @abstractmethod
    def rowcount(self): pass
    @abstractmethod
    def close(self): pass

    @abstractmethod
    def executeSelect(self, select: str, columns: Optional[ColumnList], callback: Callable[[int, Record], bool]):
        """
        Execute a SELECT query and scan the cursor calling the callback function
        and passing a Record as argument. If a column list is provided, the record
        will be created using those columns, if not, the columns will be created
        using the description of the cursor.
        :param select: The SELECT query to execute.
        :param columns: The optional column list that defines the types of the select columns.
        :param callback: The callback function that will be called with the record. The callback
        function must return a boolean indicating whether to continue execution or not.
        """
        pass
    """ End class DBCursor """
class DBConnection(ABC):
    @abstractmethod
    def get_adapter(self) -> DBAdapter: pass
    @abstractmethod
    def close(self): pass
    @abstractmethod
    def commit(self): pass
    @abstractmethod
    def rollback(self): pass
    @abstractmethod
    def cursor(self, **parameters) -> DBCursor:
        """
        Returns a cursor with the given parameters. If no parameters are given,
        the cursor must be explicitly non buffered.
        :param parameters: Cursor parameters
        :return: The cursor
        """
        pass
    """ End class DBConnection """
class DBConnectionPool(ABC):
    @abstractmethod
    def get_adapter(self) -> DBAdapter: pass
    @abstractmethod
    def get_connection(self) -> DBConnection:
        """
        Returns a connection with the given parameters. If no parameters are given,
        the connection must be explicitly not autocommit.
        :return: The connection.
        """
        pass
    @abstractmethod
    def close(self):
        """
        Explicitly close the connection pool and all connections.
        """
        pass
    """ End class DBConnectionPool """
class DB(ABC):
    def __init__(self, **parameters): pass
    @abstractmethod
    def get_adapter(self) -> DBAdapter: pass
    @abstractmethod
    def get_connection(self) -> DBConnection: pass
    @abstractmethod
    def close(self): pass
