# %%
import sqlite3
import pandas as pd
con = sqlite3.connect('database/demo_hltv.db')

cur = con.cursor()
# %%
for row in cur.execute('SELECT * FROM bronze_players'):
    print(row)
# %%
pd.read_sql_query('SELECT * FROM bronze_players LIMIT 5', con)
# %%
