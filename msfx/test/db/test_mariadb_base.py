from mariadb import ConnectionPool, Connection

pool = ConnectionPool(
    pool_name='test_back',
    pool_size=50,
    pool_validation_interval=5000,
    host='localhost', port=3306, user='root', password='carrlasass')

conn = pool.get_connection()
cursor = conn.cursor(buffered=False)

cursor.execute("SELECT * FROM qtfx_dkcp.eurusd_mn001")

count = 0
row = cursor.fetchone()
while row:
    count += 1
    print(row)
    if count >= 50: break
    row = cursor.fetchone()

print(count)
# cursor.nextset()
# cursor.close()
# conn.close()
pool.close()
print("End of test")

conn = Connection(
    host='localhost', port=3306, user='root', password='carrlasass')

cursor = conn.cursor(buffered=False)

cursor.execute("SELECT * FROM qtfx_dkcp.eurusd_mn001")

count = 0
row = cursor.fetchone()
while row:
    count += 1
    print(row)
    if count >= 50: break
    row = cursor.fetchone()

print(count)
# cursor.nextset()
# cursor.close()
conn.close()
print("End of test")
