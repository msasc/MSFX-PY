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

""" Implementation of the db_back connector interface for MariaDB. """
from mariadb import Cursor, Connection, ConnectionPool

from msfx.lib.db.cn import DBCursor, DBConnection, DBConnectionPool

class MariaDBCursor(DBCursor):
    def __init__(self, cursor: Cursor):
        self.__cursor = cursor
    def execute(self, operation, **parameters):
        self.__cursor.execute(operation, **parameters)
    def fetchone(self) -> object:
        return self.__cursor.fetchone()
    def fetchall(self) -> object:
        return self.__cursor.fetchall()
    def fetchmany(self, size=100) -> object:
        return self.__cursor.fetchmany()
    def count(self) -> int:
        return self.__cursor.rowcount
    def description(self) -> object:
        return self.__cursor.description
    def close(self):
        self.__cursor.close()

class MariaDBConnection(DBConnection):
    def __init__(self, conn: Connection):
        self.__conn = conn
    def close(self):
        self.__conn.close()
    def commit(self):
        self.__conn.commit()
    def rollback(self):
        self.__conn.rollback()
    def cursor(self, **parameters) -> DBCursor:
        return MariaDBCursor(self.__conn.cursor(**parameters))

class MariaDBConnectionPool(DBConnectionPool):
    def __init__(self, **parameters):
        self.__pool = ConnectionPool(**parameters)
    def get_connection(self) -> DBConnection:
        return MariaDBConnection(self.__pool.get_connection())
    def close(self):
        self.__pool.close()


