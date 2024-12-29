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
from typing import Optional
from datetime import time, datetime, date

from mariadb import Cursor, Connection, ConnectionPool

from msfx.lib.db import Types
from msfx.lib.db.cn import DBCursor, DBConnection, DBConnectionPool, DBAdapter
from msfx.lib.db.md import Column

class MariaDBAdapter(DBAdapter):
    def __init__(self): pass

    def get_current_date(self) -> str: return "CURRENT_DATE"

    def get_current_time(self, prec) -> str:
        current_time = "CURRENT_TIME"
        if isinstance(prec, int) and 0 < prec <= 6:
            current_time += "(" + str(prec) + ")"
        return current_time

    def get_current_datetime(self, prec) -> str:
        current_timestamp = "CURRENT_TIMESTAMP"
        if isinstance(prec, int) and 0 < prec <= 6:
            current_timestamp += "(" + str(prec) + ")"
        return current_timestamp

    def get_column(self, descr: tuple) -> Column:
        """

        ('col_varchar', 253, 20, 80, 0, 0, True, 0, 'check_types', 'col_varchar', 'check_types')
        ('col_char', 254, 1, 4, 0, 0, True, 0, 'check_types', 'col_char', 'check_types')

        ('col_tinytext', 252, 255, 1020, 0, 0, True, 16, 'check_types', 'col_tinytext', 'check_types')
        ('col_text', 252, 65535, 262140, 0, 0, True, 16, 'check_types', 'col_text', 'check_types')
        ('col_mediumtext', 252, 16777215, 67108860, 0, 0, True, 16, 'check_types', 'col_mediumtext', 'check_types')
        ('col_longtext', 252, 1073741823, -1, 0, 0, True, 16, 'check_types', 'col_longtext', 'check_types')

        ('col_tinyint', 1, 1, 4, 0, 0, True, 32768, 'check_types', 'col_tinyint', 'check_types')
        ('col_smallint', 2, 1, 6, 0, 0, True, 32768, 'check_types', 'col_smallint', 'check_types')
        ('col_mediumint', 9, 2, 9, 0, 0, True, 32768, 'check_types', 'col_mediumint', 'check_types')
        ('col_int', 3, 2, 11, 0, 0, True, 32768, 'check_types', 'col_int', 'check_types')
        ('col_bigint', 8, 5, 20, 0, 0, True, 32768, 'check_types', 'col_bigint', 'check_types')

        ('col_float', 4, 3, 12, 0, 0, True, 32768, 'check_types', 'col_float', 'check_types')
        ('col_double', 5, 5, 22, 0, 0, True, 32768, 'check_types', 'col_double', 'check_types')
        ('col_decimal', 246, 23, 22, 22, 6, True, 32768, 'check_types', 'col_decimal', 'check_types')

        ('col_varbinary', 253, 5, 20, 0, 0, True, 128, 'check_types', 'col_varbinary', 'check_types')
        ('col_binary', 254, 5, 20, 0, 0, True, 128, 'check_types', 'col_binary', 'check_types')

        ('col_tinyblob', 252, 63, 255, 0, 0, True, 144, 'check_types', 'col_tinyblob', 'check_types')
        ('col_blob', 252, 16383, 65535, 0, 0, True, 144, 'check_types', 'col_blob', 'check_types')
        ('col_mediumblob', 252, 4194303, 16777215, 0, 0, True, 144, 'check_types', 'col_mediumblob', 'check_types')
        ('col_longblob', 252, 1073741823, -1, 0, 0, True, 144, 'check_types', 'col_longblob', 'check_types')

        ('col_date', 10, 2, 10, 0, 0, True, 128, 'check_types', 'col_date', 'check_types')
        ('col_time', 11, 2, 10, 0, 0, True, 128, 'check_types', 'col_time', 'check_types')
        ('col_year', 13, 1, 4, 0, 0, True, 32864, 'check_types', 'col_year', 'check_types')
        ('col_datetime', 12, 4, 19, 0, 0, True, 128, 'check_types', 'col_datetime', 'check_types')
        ('col_timestamp', 7, 4, 19, 0, 0, True, 160, 'check_types', 'col_timestamp', 'check_types')

        """
        column_alias: str = descr[0]
        t_code: int = descr[1]
        length: int = descr[2]
        i_length: int = descr[3]
        precision: int = descr[4]
        scale: int = descr[5]
        nullable: bool = descr[6]
        t_ext: int = descr[7]
        table_alias = descr[8]
        column_name = descr[9]
        table_name = descr[10]

        # Determine the root of the database type.

        db_type: Optional[str] = None
        if t_code == 253 and t_ext == 0: db_type = "VARCHAR"
        elif t_code == 254 and t_ext == 0: db_type = "CHAR"

        elif t_code == 252 and t_ext == 16 and length == 255: db_type = "TINYTEXT"
        elif t_code == 252 and t_ext == 16 and length == 65535: db_type = "TEXT"
        elif t_code == 252 and t_ext == 16 and length == 16777215: db_type = "MEDIUMTEXT"
        elif t_code == 252 and t_ext == 16 and length == 1073741823: db_type = "LONGTEXT"

        elif t_code == 1 and t_ext == 32768: db_type = "TINYINT"
        elif t_code == 2 and t_ext == 32768: db_type = "SMALLINT"
        elif t_code == 9 and t_ext == 32768: db_type = "MEDIUMINT"
        elif t_code == 3 and t_ext == 32768: db_type = "INT"
        elif t_code == 8 and t_ext == 32768: db_type = "BIGINT"

        elif t_code == 4 and t_ext == 32768: db_type = "FLOAT"
        elif t_code == 5 and t_ext == 32768: db_type = "DOUBLE"
        elif t_code == 246 and t_ext == 32768: db_type = "DECIMAL"

        elif t_code == 253 and t_ext == 128: db_type = "VARBINARY"
        elif t_code == 254 and t_ext == 128: db_type = "BINARY"

        elif t_code == 252 and t_ext == 144 and i_length == 255: db_type = "TINYBLOB"
        elif t_code == 252 and t_ext == 144 and i_length == 65535: db_type = "BLOB"
        elif t_code == 252 and t_ext == 144 and i_length == 16777215: db_type = "MEDIUMBLOB"
        elif t_code == 252 and t_ext == 144 and i_length == -1: db_type = "LONGBLOB"

        elif t_code == 10 and t_ext == 128: db_type = "DATE"
        elif t_code == 11 and t_ext == 128: db_type = "TIME"
        elif t_code == 12 and t_ext == 128: db_type = "DATETIME"
        elif t_code == 7 and t_ext == 160: db_type = "TIMESTAMP"

        if db_type is None: raise TypeError("Not supported database type {}".format(t_code))

        # Determine this library type.

        column_type: Optional[Types] = None
        if db_type in ("VARCHAR", "CHAR", "TINYTEXT", "TEXT", "MEDIUMTEXT", "LONGTEXT"):
            column_type = Types.STRING
        if db_type in ("TINYINT", "SMALLINT", "MEDIUMINT", "INT", "BIGINT"):
            column_type = Types.INTEGER
        if db_type in ("FLOAT", "DOUBLE"):
            column_type = Types.FLOAT
        if db_type == "DECIMAL":
            column_type = Types.DECIMAL
        if db_type in ("VARBINARY", "BINARY", "TINYBLOB", "BLOB", "MEDIUMBLOB", "LONGBLOB"):
            column_type = Types.BINARY
        if db_type == "DATE":
            column_type = Types.DATE
        if db_type == "TIME":
            column_type = Types.TIME
        if db_type in ("DATETIME", "TIMESTAMP"):
            column_type = Types.DATETIME

        if column_type is None: raise TypeError("Not supported database type {}".format(db_type))

        # Complete the database type if required.

        column = Column()
        column.set_name(column_name)
        column.set_alias(column_alias)
        column.set_type(column_type)

        column.set_table_name(table_name)
        column.set_table_alias(table_alias)
        column.set_db_type(db_type)


        return column

    def get_column_db_def(self, column: Column) -> str:
        """ Returns the database column definition as a string. """
        return ""
    def get_lib_type(self, db_type: str) -> Types:
        return Types.STRING
    def to_sql_binary(self, value: (bytes, bytearray)) -> str:
        return ""
    def to_sql_date(self, value: date) -> str:
        return ""
    def to_sql_datetime(self, value: datetime) -> str:
        return ""
    def to_sql_time(self, value: time) -> str:
        return ""


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


