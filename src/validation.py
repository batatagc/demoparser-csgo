import sqlite3

con = sqlite3.connect('database/demo_hltv.db')

cur = con.cursor()

for row in cur.execute('SELECT count(*) FROM bronze_matches WHERE demo_id is null'):
    print(row)