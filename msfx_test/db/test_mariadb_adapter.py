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
from msfx.db.adapters.adapter_mariadb import MariaDBConnection, MariaDBIterator

try:
    cn = MariaDBConnection(user="root", password="carrlasass", host="127.0.0.1")

    rs = cn.iterator("SELECT * FROM qtfx_dkcp.eurusd_dy001 ORDER BY time")
    n = 0
    while rs.has_next():
        n += 1
        rc = rs.next()
        print(f"{n} --- {rc.get_value('time')}, {rc.get_value('open')}, {rc.get_value('close')}")

    rs = cn.iterator("SELECT COUNT(*) FROM qtfx_dkcp.eurusd_dy001")
    while rs.has_next():
        rc = rs.next()
        print(f"Count --- {rc.get_value('COUNT(*)')}")

    print(rs.is_closed())
    print(cn.is_closed())

    rows = cn.execute("UPDATE qtfx_dkcp.eurusd_dy001 SET close = close")
    print(rows)

    cn.close()
    print(cn.is_closed())

except Exception as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)
