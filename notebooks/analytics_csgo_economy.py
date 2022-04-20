# %%
from cProfile import label
import os
import json
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
df_rounds = demo_parser._parse_rounds()
# %%
df_game_rounds = df_rounds[df_rounds['winningSide'].isin(['CT','T'])][df_rounds['freezeTimeEndTick']!=0][df_rounds['ctRoundStartMoney']!=0].reset_index().copy()
# %%
df_game_rounds['winningSide'].value_counts() / df_game_rounds['winningSide'].value_counts().sum()
# %%
fig, ax = plt.subplots(figsize=(15,6))

sns.lineplot(x=df_game_rounds.index, y=df_game_rounds['tStartEqVal'], color='#DAA520', label='Terrorists', ax=ax)

sns.lineplot(x=df_game_rounds.index, y=df_game_rounds['ctStartEqVal'], color='#4682B4', label='Counter-Terrorists', ax=ax)
# %%
json_file = os.path.join(NOTEBOOKS_DIR, "timemlopes__vs__timepurpz.json")
f = open(json_file)

json_match = json.load(f)

half_tick = json_match['matchPhases']['gameHalfEnded'][0]
# %%
df_game_rounds['gameHalf'] = (df_game_rounds['startTick']>=half_tick).astype('int') + 1
# %%
team1 = df_game_rounds['tTeam'][0]
team2 = df_game_rounds['ctTeam'][0]
# %%
df_game_rounds.rename(columns={'endCTScore':'ctEndScore', 'endTScore':'tEndScore'}, inplace=True)

t_cols = [col for col in df_game_rounds.columns if col.startswith('t')]
ct_cols = [col for col in df_game_rounds.columns if col.startswith('ct')]

df_team_1_t = df_game_rounds[df_game_rounds['tTeam']==team1][t_cols]
df_team_1_ct = df_game_rounds[df_game_rounds['ctTeam']==team1][ct_cols]

df_team_1_t.columns = ['team1'+col[1:] for col in df_team_1_t.columns]
df_team_1_ct.columns = ['team1'+col[2:] for col in df_team_1_ct.columns]
# %%
df_team_2_t = df_game_rounds[df_game_rounds['tTeam']==team2][t_cols]
df_team_2_ct = df_game_rounds[df_game_rounds['ctTeam']==team2][ct_cols]

df_team_2_t.columns = ['team2'+col[1:] for col in df_team_2_t.columns]
df_team_2_ct.columns = ['team2'+col[2:] for col in df_team_2_ct.columns]

# %%
df_team_1 = df_team_1_t.append(df_team_1_ct)
df_team_2 = df_team_2_t.append(df_team_2_ct)
# %%
df_rounds_info = df_game_rounds[['winningSide','winningTeam','losingTeam','roundEndReason','gameHalf']]
# %%
df_team_1.sort_index()
# %%
df_team_2.sort_index()
# %%
df_rounds_results = df_rounds_info.merge(df_team_1, left_index=True, right_index=True).merge(df_team_2, left_index=True, right_index=True)
df_rounds_results['Vitory'] = [i[1]['team1RoundStartMoney'] if i[1]['winningTeam']==i[1]['team1Team'] else i[1]['team2RoundStartMoney'] for i in df_rounds_results.iterrows()]
# %%
sns.set()

fig, ax = plt.subplots(figsize=(15,6))

sns.lineplot(x=df_team_1.index, y=df_team_1['team1RoundStartMoney'], color='#DAA520', label=df_team_1['team1Team'].iloc[0], ax=ax)

sns.lineplot(x=df_team_2.index, y=df_team_2['team2RoundStartMoney'], color='#4682B4', label=df_team_2['team2Team'].iloc[0], ax=ax)

sns.scatterplot(x=df_rounds_results.index, y=df_rounds_results['Vitory'], color='#000000', ax=ax)

ax.legend()
# %%
df_rounds_results[['winningSide', 'winningTeam', 'roundEndReason', 'gameHalf', 'team1BuyType', 'team2BuyType']]
# %%
df_rounds_results.groupby(['winningTeam'])['team2BuyType'].value_counts()
# %%
df_rounds_results.groupby(['winningTeam'])['team1BuyType'].value_counts()