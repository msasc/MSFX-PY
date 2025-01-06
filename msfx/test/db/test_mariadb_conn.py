from mariadb import ConnectionPool, Connection

conn = Connection(
    host='localhost', port=3306, user='root', password='carrlasass')

cursor = conn.cursor(buffered=False)

cursor.execute("SELECT * FROM qtfx_dkcp.eurusd_hr001")

count = 0
row = cursor.fetchone()
while row:
    count += 1
    print(row)
    if count >= 50: break
    row = cursor.fetchone()

print(count)
cursor.close()
conn.close()
print("End of test")
