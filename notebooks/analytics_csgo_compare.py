# %%
import os
import pandas as pd
import matplotlib.pyplot as plt
from pyparsing import alphas
import seaborn as sns
import numpy as np

from awpy import DemoParser

NOTEBOOKS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(NOTEBOOKS_DIR)
DEMOS_DIR = os.path.join(BASE_DIR, "demos")
MAPS_DIR = os.path.join(BASE_DIR, "maps")
# %%
demofile = os.path.join(DEMOS_DIR, "2022-03-26__0007__1__15477821__de_train__timemlopes__vs__timepurpz.dem")
demo_parser = DemoParser(demofile=demofile, demo_id="timemlopes__vs__timepurpz", parse_rate=128)

demo_parser.parse()
# %%
df_kills = demo_parser._parse_kills()
# %%
df_qtKills = df_kills[['attackerName', 'victimName']].value_counts().reset_index().rename(columns={0: 'qtKills',}).sort_values(by='attackerName', ascending=False)
# %%
df_compare = (df_qtKills.merge(df_qtKills, left_on=['attackerName','victimName'], right_on=['victimName','attackerName'], how='outer')
          .rename(columns={'attackerName_x': 'attackerName', 'victimName_x': 'victimName', 'qtKills_x': 'qtKills', 'qtKills_y': 'qtDeaths'})
          .drop(columns=['attackerName_y', 'victimName_y'])
          .sort_values(by='attackerName', ascending=False)
          .fillna(0)
          .astype({'qtKills': int, 'qtDeaths': int}))

# '★ ⑮ batata', '★ ⑭ LioN', '★ ⑭ Xilanta', '★ ⑩ Roger do Roger That', '★ ④ Coelho', '★ ④ mlopes', '★ ⑭ purpz', '★ ⑥ chellesChelles', '★ ⑭ Campeiro', '★ ③ TeoMeWhy'
nick = '★ ⑭ Xilanta'
# %%
def highlight_max(s, props=''):
    return np.where(s > np.nanmin(s.values), props, 'color:white;background-color:#A9A9A9')

df_compare_color = df_compare[df_compare['attackerName'] == nick][['victimName','qtKills', 'qtDeaths']].set_index('victimName').style.apply(highlight_max, props='color:white;background-color:#1E90FF', axis=1)
df_compare_color
# %%
