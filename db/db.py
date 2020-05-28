# https://www.youtube.com/watch?v=2PDkXviEMD0&t=442s
import psycopg2

# connect to the db
con = psycopg2.connect(
    host = '192.168.0.59',
    database = 'dejavu',
    user = 'postgres',
    password = 'password')

# cursor
cur = con.cursor()

# 테이블 만들기
command = (
    '''
    CREATE TABLE vendors(
        vendor_id SERIAL PRIMARY KEY,
        vendor_name VARCHAR(255) NOT NULL
    )
    ''')
# 가져오기
selects = '''
SELECT vendor_id, vendor_name FROM vendors
'''

# execute query
# cur.execute(command)
cur.execute(selects)

rows = cur.fetchall()

for r in rows:
    print( f"id {r[0]} name {r[1]}" )

# close the cursor
cur.close()

# close the connection
con.close()