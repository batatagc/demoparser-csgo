from typing import List
import requests
from lxml import html
import time
import sqlite3
from datetime import datetime 

con = sqlite3.connect('database/demo_hltv.db')

cur = con.cursor()

cur.execute('SELECT * FROM bronze_matches')

results = cur.fetchall()

for match in results:

    match_id = match[0]
    description = match[1]
    updated_at = datetime.now().__str__()

    url = f'https://www.hltv.org/matches/{match_id}/{description}'

    r = requests.get(url=url)

    tree = html.fromstring(r.content)

    demo = tree.xpath(f"//div[contains(@class, 'stream-box')]/a/@href")

    demo_id = demo[0].split('/')[3]

    cur.execute(f"UPDATE bronze_matches SET demo_id = {demo_id}, updated_at = '{updated_at}' WHERE match_id = {match_id}")
    
    con.commit()

    time.sleep(1)