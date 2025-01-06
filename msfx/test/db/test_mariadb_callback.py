from msfx.lib import MutableDecimal
from msfx.lib.db.cn.mariadb import MariaDB
from msfx.lib.db.rs import Record

db = MariaDB(
    pool_name='test_back',
    pool_size=50,
    pool_validation_interval=5000,
    host='localhost', port=3306, user='root', password='carrlasass')

conn = db.get_connection()
cursor = conn.cursor()

counter = MutableDecimal()
def callback(count: int, rec: Record) -> bool:
    counter.add(1)
    print("#{}, {}".format(count, rec))
    return True

cursor.executeSelect("SELECT * FROM qtfx_dkcp.eurusd_hr004", None, callback)

cursor.close()
conn.close()
db.close()

print(counter)
