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

try:
	conn = mariadb.connect(
		user="root", password="carrlasass", host="127.0.0.1"
	)

	cur = conn.cursor(buffered=False)
	# cur.execute("SELECT COUNT(*) FROM qtfx_dkcp.eurusd_mn001")
	# print(cur.next())

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

	for column in cur.description:
		column_name = column[0]
		column_type = field_info.type(column)
		column_flags = field_info.flag(column)
		print(f"{column}")

	print("".join("-" for n in range(150)))
	print("".join("-" for n in range(150)))

	sql = "SHOW FULL COLUMNS FROM qtest.types"
	cur.execute(sql)

	while True:
		rec = cur.next()
		if rec is None: break
		print(f"{rec}")

	sql = "DROP TABLE IF EXISTS qtest.types"
	cur.execute(sql)

	cur.close()
	conn.close()

except mariadb.Error as e:
	print(f"Error connecting to MariaDB Platform: {e}")
	sys.exit(1)
