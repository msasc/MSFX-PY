from msfx.lib.db.cn.mariadb import MariaDB

db = MariaDB(
    pool_name='test_back',
    pool_size=50,
    pool_validation_interval=5000,
    host='localhost', port=3306, user='root', password='carrlasass')

conn = db.get_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM qtfx_dkcp.eurusd_hr001")

adapter = db.get_adapter()
columns = []
for col_descr in cursor.description:
    print(col_descr)
    columns.append(adapter.get_column_from_cursor_descr(col_descr))

count = 0
row = cursor.fetchone()
while row:
    count += 1
    print(row)
    if count >= 50: break
    row = cursor.fetchone()

print(count)
print(cursor.count())

cursor.close()
cursor.close()
conn.close()
db.close()

