from mariadb import ConnectionPool

pool = ConnectionPool(pool_name='test', host='localhost', user='root', password='carrlasass')
conn = pool.get_connection()

cursor = conn.cursor(buffered=False)
cursor.execute("SELECT * FROM qtfx_dkcp.eurusd_mn001")

count = 0
# batch_size = 100
# rows = cursor.fetchmany(batch_size)
# while rows:
#     for row in rows:
#         count += 1
#         print(row)  # Process each row
#         if count >= 1000: break
#     if count >= 1000: break
#     rows = cursor.fetchmany(batch_size)

print("OK")
print(cursor.rowcount)
# print("Column names and types:")
# for column in cursor.description:
#     print(f"Column: {column[0]}, Type: {type(column[1])}")
#
# print()

row = cursor.fetchone()
while row is not None:
    count += 1
    print(row)
    if count >= 1000000: break
    row = cursor.fetchone()
print(cursor.rowcount)

cursor.close()
conn.close()
pool.close()