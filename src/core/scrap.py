import requests
import os
from lxml import html
import sqlite3
from datetime import datetime
import time

class ScrapHLTV():
    def __init__(self, offset=None):
        self.offset = offset
        self.matches = None
        self.con = None
        self.cur = None

    def create_connection(self):
        self.con = sqlite3.connect('database/demo_hltv.db')
        self.cur = self.con.cursor()
        return

    def create_dir(self, dir_name=None):
        try:
            os.mkdir(dir_name)
        except FileExistsError:
            pass
        return

    def prepare(self):
        list_dir = ['database']
        for dir_name in list_dir:
            self.create_dir(dir_name=dir_name)
        return

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS bronze_matches (
                    match_id int,
                    description text,
                    demo_id int,
                    created_at timestamp,
                    updated_at timestamp,
                    PRIMARY KEY (match_id) 
                )
                """)
        self.con.commit()
        return

    def get_matches(self):
        url = f'https://www.hltv.org/results?offset={self.offset}'
        r = requests.get(url=url)
        tree = html.fromstring(r.content)
        self.matches = tree.xpath(f"//div[contains(@class, 'result-con')]/a/@href")
        return
    
    def save_matches(self):
        print(f"Saving matches from offset {self.offset} ... ", end="")
        created_at = datetime.now().__str__()
        matches_splited = [ match.split('/') for match in self.matches ]
        for match in matches_splited:
            if len(match) > 3:
                self.cur.execute(f"""INSERT INTO bronze_matches 
                                VALUES (
                                    {match[2]}, 
                                    '{match[3]}', 
                                    NULL, 
                                    '{created_at}', 
                                    '{created_at}' 
                                ) 
                                ON CONFLICT DO NOTHING;
                                """)
                self.con.commit()
        print("Done")
        return

    def update_demos(self):
        print("Updating Demos ... ", end="")
        self.cur.execute("""SELECT * 
                            FROM bronze_matches
                            WHERE demo_id is NULL
                        """)
        results = self.cur.fetchall()

        for match in results:
            match_id = match[0]
            description = match[1]
            updated_at = datetime.now().__str__()

            url = f'https://www.hltv.org/matches/{match_id}/{description}'
            r = requests.get(url=url)

            tree = html.fromstring(r.content)

            demo = tree.xpath(f"//div[contains(@class, 'stream-box')]/a/@href")
            
            if len(demo) > 0:
                if len(demo[0]) > 3:
                    demo_id = demo[0].split('/')[3]

                    self.cur.execute(f"""UPDATE bronze_matches 
                                        SET demo_id =     {demo_id}, 
                                            updated_at = '{updated_at}' 
                                        WHERE match_id = {match_id}
                                    """)
                self.con.commit()
                time.sleep(0.25)
        print("Done")

    def start(self):
        print("Preparing scraping ...", end="")
        self.prepare()
        self.create_connection()
        self.create_table()
        self.get_matches()
        print("OK")
        self.save_matches()
        self.update_demos()
        return