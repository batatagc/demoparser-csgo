import sqlite3
from datetime import datetime

con = sqlite3.connect('database/demo_hltv.db')

cur = con.cursor()

cur.execute('''DROP TABLE bronze_matches''')

cur.execute('''CREATE TABLE bronze_matches (
                    match_id int,
                    description text,
                    demo_id int,
                    created_at timestamp,
                    updated_at timestamp,
                    PRIMARY KEY (match_id) 
                )
                ''')

created_at = datetime.now().__str__()

cur.execute(f"INSERT INTO bronze_matches VALUES (2355752, 'faze-vs-mouz-pgl-major-antwerp-2022-europe-rmr-a', 71453,'{created_at}', '{created_at}')")

con.commit()

con.close()
