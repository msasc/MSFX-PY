
from msfx.lib_back2.db.cn.mariadb import MariaDBConnectionPool

pool = MariaDBConnectionPool(
    pool_name='test_back',
    pool_size=50,
    pool_validation_interval=5000,
    host='localhost', user='root', password='carrlasass')
conn = pool.get_connection()
cursor = conn.cursor(buffered=False)

cursor.execute("SELECT * FROM qtfx_dkcp.eurusd_mn001")

count = 0
row = cursor.fetchone()
while row is not None:
    count += 1
    print(row)
    if count >= 1000: break
    row = cursor.fetchone()

print(cursor.count())

cursor.close()
conn.close()
pool.close()

