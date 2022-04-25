# %%
import os
import json
from numpy import append
import pandas as pd
import sqlite3
# %%
json_file = 'demos-parsed/71396_1.json'
with open(json_file) as f:
    data = json.load(f)

con = sqlite3.connect('database/demo_hltv.db')
# %%
class SplitDemo():
    def __init__(self, data) -> None:
        self.data = data
        pass

    def rounds(self, con):
        match = data['matchID']
        mapname = data['mapName']

        columns = ['matchID', 'mapName', 'roundNum', 'isWarmup', 'tScore', 'ctScore', 
                'endTScore', 'endCTScore', 'ctTeam', 'tTeam',
                'winningSide', 'winningTeam', 'losingTeam', 
                'roundEndReason', 'ctStartEqVal', 'ctRoundStartEqVal', 
                'ctRoundStartMoney', 'ctBuyType', 'ctSpend', 'tStartEqVal', 
                'tRoundStartEqVal', 'tRoundStartMoney', 'tBuyType', 'tSpend']

        rounds = []
        for round in data['gameRounds']:
            round_info = []
            for match_info in [match, mapname]:
                round_info.append(match_info)
            for field in round.keys():
                if field in columns:
                    round_info.append(round[field])
            rounds.append(round_info)

        df_rounds = pd.DataFrame(rounds, columns=columns)
        df_rounds.to_sql('bronze_rounds', con=con, if_exists='append', index=False)
        return

    def tick_rate(self, con):
        match = data['matchID']
        columns = ['matchID','roundNum','tick', 'seconds', 'clockTime', 'bombPlanted', 'bombsite']
        columns_side = ['side', 'teamEqVal', 'alivePlayers', 'totalUtility']
        rounds = []
        for round in data['gameRounds']:
            for frame in round['frames']:
                frame_info = []
                frame_info.append(match)
                frame_info.append(round['roundNum'])
                for field in frame.keys():
                    if field in columns:
                        frame_info.append(frame[field])
                for side in ['t', 'ct']:
                    for field in frame[side].keys():
                        if field in columns_side:
                            frame_info.append(frame[side][field])
                rounds.append(frame_info)

        columns_sides = [col + '_' + side for side in ['t', 'ct'] for col in columns_side]

        df_tick = pd.DataFrame(rounds, columns=[*columns, *columns_sides])
        df_tick.to_sql('bronze_ticks', con=con, if_exists='append', index=False)
        return 

    def players(self, con):
        match = data['matchID']
        columns = ['matchID','roundNum','steamID','hp','armor',
                    'totalUtility','isAlive','isInBombZone','equipmentValue',
                    'cash','hasHelmet','hasDefuse','hasBomb']

        players = []
        for round in data['gameRounds']:
            for frame in round['frames']:
                for player in frame['t']['players']:
                    players_info = []
                    players_info.append(match)
                    players_info.append(round['roundNum'])
                    for key in player.keys():
                        if key in columns:
                            players_info.append(player[key])   
                    players.append(players_info)

        df_players = pd.DataFrame(players, columns=columns)
        df_players.to_sql('bronze_players', con=con, if_exists='append', index=False)

    def start(self, con):
        self.rounds(con)
        self.tick_rate(con)
        self.players(con)
        return
# %%
SplitDemo(data).start(con)
# %%
match = data['matchID']
columns = ['matchID','roundNum','steamID','hp','armor','totalUtility','isAlive','isInBombZone','inventory','equipmentValue','cash','hasHelmet','hasDefuse','hasBomb']
inventory_columns = ['primary', 'pistol', 'flashbang' 'molotov', 'grenade', 'smoke', 'decoy']
players = []
for round in data['gameRounds']:
    for frame in round['frames']:
        for player in frame['t']['players']:
            players_info = []
            players_info.append(match)
            players_info.append(round['roundNum'])
            for key in player.keys():
                if key in columns:
                    players_info.append(player[key])   
                if key in ["inventory"]:
                    if player[key] is not None:
                        for item in player[key]:
                            if item['weaponClass'] in ['Rifle','SMG','Heavy']:
                                players_info.append(item['weaponClass'])                            
                            if item['weaponClass'] == 'Pistols':
                                players_info.append(item['weaponName'])
                            if item['weaponName'] == 'Flashbang':
                                players_info.append(item['ammoInMagazine'] + item['ammoInReserve'])

                            if item['weaponName'] == 'Molotov':
                                players_info.append(item['ammoInMagazine'])

                            if item['weaponName'] == 'HE Grenade':
                                players_info.append(item['ammoInMagazine'])
                            
                            if item['weaponName'] == 'Smoke Grenade':
                                players_info.append(item['ammoInMagazine'])
                            
                            if item['weaponName'] == 'Decoy Grenade':
                                players_info.append(item['ammoInMagazine'])
                            else:
                                players_info.append(0)

            players.append(players_info)

df_players = pd.DataFrame(players, columns=[*columns, *inventory_columns])
df_players
# %%

