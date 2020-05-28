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

# execute query
cur.execute('select id, name from employees')

rows = cur.fetchall()

for r in rows:
    print( f"id {r[0]} name {r[1]}" )

# close the cursor
cur.close()

# close the connection
con.close()