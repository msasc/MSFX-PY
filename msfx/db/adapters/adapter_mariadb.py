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
""" MariaDB adapter."""

from msfx.db.cn import Connection
from msfx.db.data import Types, Field, Fields, RecordIterator, Record

import mariadb
from abc import ABC

def _get_field_(field_info: mariadb.fieldinfo, column: tuple) -> Field:
    field = Field()
    field.set_name(column[0])

    ntype = column[1]
    nlength = column[3]
    ndecs = column[5]
    tflags = field_info.flag(column)

    binary: bool = True if tflags.find("BINARY") >= 0 else False

    if ntype == 1:
        field.set_type(Types.BOOLEAN)
        field.get_properties()["DB_TYPE"] = "TINYINT"
    if ntype == 3:
        field.set_type(Types.INTEGER)
        field.get_properties()["DB_TYPE"] = "INTEGER"
    if ntype == 4:
        field.set_type(Types.FLOAT)
        field.get_properties()["DB_TYPE"] = "FLOAT"
    if ntype == 5:
        field.set_type(Types.FLOAT)
        field.get_properties()["DB_TYPE"] = "DOUBLE"
    if ntype == 8:
        field.set_type(Types.INTEGER)
        field.get_properties()["DB_TYPE"] = "BIGINT"
    if ntype == 246:
        field.set_type(Types.DECIMAL)
        field.set_length(nlength - 2)
        field.set_decimals(ndecs)
        field.get_properties()["DB_TYPE"] = "DECIMAL"
        field.get_properties()["DB_LENGTH"] = nlength - 2
        field.get_properties()["DB_DECIMALS"] = ndecs
    if ntype == 252:
        if binary:
            field.set_type(Types.BINARY)
            if nlength == 255: field.get_properties()["DB_TYPE"] = "TINYBLOB"
            if nlength == 65535: field.get_properties()["DB_TYPE"] = "BLOB"
            if nlength == 16777215: field.get_properties()["DB_TYPE"] = "MEDIUMBLOB"
            if nlength == -1: field.get_properties()["DB_TYPE"] = "LONGBLOB"
        else:
            field.set_type(Types.STRING)
            if nlength == 255: field.get_properties()["DB_TYPE"] = "TINYTEXT"
            if nlength == 65535: field.get_properties()["DB_TYPE"] = "TEXT"
            if nlength == 16777215: field.get_properties()["DB_TYPE"] = "MEDIUMTEXT"
            if nlength == -1: field.get_properties()["DB_TYPE"] = "LONGTEXT"
        if nlength > 0: field.set_length(nlength)
        field.get_properties()["DB_LENGTH"] = nlength
    if ntype == 253:
        if binary:
            field.set_type(Types.BINARY)
            field.get_properties()["DB_TYPE"] = "VARBINARY"
        else:
            field.set_type(Types.STRING)
            field.get_properties()["DB_TYPE"] = "VARCHAR"
        field.set_length(nlength)
        field.get_properties()["DB_LENGTH"] = nlength
    if ntype == 254:
        field.set_type(Types.BINARY)
        field.set_length(nlength)
        field.get_properties()["DB_TYPE"] = "BINARY"
        field.get_properties()["DB_LENGTH"] = nlength
    if ntype == 10:
        field.set_type(Types.DATE)
        field.get_properties()["DB_TYPE"] = "DATE"
        field.get_properties()["DB_LENGTH"] = nlength
    if ntype == 11:
        field.set_type(Types.TIME)
        field.get_properties()["DB_TYPE"] = "TIME"
        field.get_properties()["DB_LENGTH"] = nlength
    if ntype == 12:
        field.set_type(Types.DATETIME)
        field.get_properties()["DB_TYPE"] = "DATETIME"
        field.get_properties()["DB_LENGTH"] = nlength

    return field

class MariaDBIterator: pass

class MariaDBConnection(Connection):
    def __init__(self, **params):
        m_user = params.get("user")
        m_password = params.get("password")
        m_host = params.get("host")
        m_database = params.get("database")
        self.__cn = mariadb.connect(
            user=m_user, password=m_password, host=m_host, database=m_database
        )

    def close(self): self.__cn.close()
    def is_closed(self) -> bool: return self.__cn._closed
    def is_auto_commit(self) -> bool: return self.__cn.autocommit
    def set_auto_commit(self, auto_commit: bool): self.__cn.autocommit = True
    def begin(self): self.__cn.begin()
    def commit(self): self.__cn.commit()
    def rollback(self): self.__cn.rollback()

    def iterator(self, select: str) -> RecordIterator:
        cursor = self.__cn.cursor(buffered=False)
        cursor.execute(select)
        if not cursor.description:
            cursor.close()
            raise Exception("Argument select is not a select query.")
        iterator = MariaDBIterator(cursor)
        return iterator

    def execute(self, command: str) -> int:
        cursor = self.__cn.cursor(buffered=False)
        cursor.execute(command)
        if cursor.description:
            cursor.close()
            raise Exception("Argument command is not an SQL command.")
        return cursor.affected_rows

class MariaDBIterator(RecordIterator):
    def __init__(self, cursor: mariadb.cursors.Cursor):
        self.__cursor = cursor
        self.__record: tuple = None
        # Build the list of fields.
        field_info = mariadb.fieldinfo()
        self.__fields = Fields()
        for column in cursor.description:
            self.__fields.append_field(_get_field_(field_info, column))
    def has_next(self) -> bool:
        self.__record = self.__cursor.fetchone()
        if not self.__record:
            self.close()
            return False
        return True
    def next(self) -> Record:
        if not self.__record: raise StopIteration("End of iterator has been reached.")
        record = Record(self.__fields, list(self.__record))
        return record
    def close(self) -> None:
        if not self.__cursor.closed: self.__cursor.close()
    def is_closed(self) -> bool:
        return self.__cursor.closed

