from typing import List
import requests
from lxml import html
import sqlite3
from datetime import datetime

offset = 0

for offset in [0, 100, 200]:

    url = f'https://www.hltv.org/results?offset={offset}'

    r = requests.get(url=url)

    tree = html.fromstring(r.content)

    matches = tree.xpath(f"//div[contains(@class, 'result-con')]/a/@href")

    matches_links = [ match.split('/') for match in matches ]

    con = sqlite3.connect('database/demo_hltv.db')

    cur = con.cursor()

    created_at = datetime.now().__str__()

    for match in matches_links:
        cur.execute(f"INSERT INTO bronze_matches VALUES ({match[2]}, '{match[3]}', NULL, '{created_at}', '{created_at}' ) ON CONFLICT DO NOTHING;")

    con.commit()

    con.close()