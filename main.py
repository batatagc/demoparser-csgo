import awpy
import sqlite3
from src.core.process import DemoPipeline

con = sqlite3.connect('database/demo_hltv.db')

cur = con.cursor()

query = """SELECT * FROM bronze_matches WHERE demo_id is not null LIMIT 20"""

matches = cur.execute(query).fetchall()

for match in matches:
    demo_id = match[2]
    description = match[1]
    match_id = match[0]

    DemoPipeline(demo_id=demo_id, 
                 description=description,
                 match_id=match_id, 
                 rate=128).start()