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

import sys
import mariadb

from msfx.db.data import Types, Field

def get_field(column: tuple) -> Field:

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

try:
    conn = mariadb.connect(
        user="root", password="carrlasass", host="127.0.0.1"
    )

    cur = conn.cursor(buffered=False)

    sql = "CREATE DATABASE IF NOT EXISTS qtest"
    cur.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS qtest.types ("
    sql += "type_pk_01 INTEGER UNIQUE KEY, "
    sql += "type_pk_02 VARCHAR(20) UNIQUE KEY, "
    sql += "type_boolean BOOLEAN, "
    sql += "type_decimal DECIMAL(20,4), "
    sql += "type_decimal2 DECIMAL(50,10), "
    sql += "type_integer INTEGER, "
    sql += "type_long BIGINT, "
    sql += "type_float FLOAT, "
    sql += "type_double DOUBLE, "
    sql += "type_bynary BINARY(100), "
    sql += "type_tinyblob TINYBLOB, "
    sql += "type_blob BLOB, "
    sql += "type_mediumblob MEDIUMBLOB, "
    sql += "type_longblob LONGBLOB, "
    sql += "type_tinytext TINYTEXT, "
    sql += "type_text TEXT, "
    sql += "type_mediumtext MEDIUMTEXT, "
    sql += "type_longtext LONGTEXT, "
    sql += "type_json JSON, "
    sql += "type_varbinary VARBINARY(100), "
    sql += "type_varchar VARCHAR(100), "
    sql += "type_date DATE, "
    sql += "type_time TIME, "
    sql += "type_datetime DATETIME "
    sql += ")"
    cur.execute(sql)

    sql = "SELECT * FROM qtest.types"
    cur.execute(sql)

    field_info = mariadb.fieldinfo()
    fields = []

    for column in cur.description:
        column_name = column[0]
        column_type = field_info.type(column)
        column_flags = field_info.flag(column)

        print(f"{column} --- {column_name} --- {column_type} --- {column_flags}")
        fields.append(get_field(column))

    print("".join("-" for n in range(150)))
    print("".join("-" for n in range(150)))

    for field in fields:
        print(f"{field}")

    sql = "DROP TABLE IF EXISTS qtest.types"
    cur.execute(sql)

    sql = "DROP DATABASE IF EXISTS qtest"
    cur.execute(sql)

except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)
