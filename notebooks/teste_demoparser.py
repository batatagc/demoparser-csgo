# %%
import os
import pandas as pd

from awpy import DemoParser

NOTEBOOKS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(NOTEBOOKS_DIR)
DEMOS_DIR = os.path.join(BASE_DIR, "demos")
# %%
class DemoParserGC(DemoParser):
    def __init__(self, demofile="", outpath=None, log=False, demo_id=None, parse_rate=128, parse_frames=True, trade_time=5, dmg_rolled=False, buy_style="hltv", json_indentation=False):
        super().__init__(demofile, outpath, log, demo_id, parse_rate, parse_frames, trade_time, dmg_rolled, buy_style, json_indentation)

    def _parse_player_inventory_frames(self):
        if self.json:
            player_frames = []
            for r in self.json["gameRounds"]:
                if r["frames"]:
                    for frame in r["frames"]:
                        for side in ["ct", "t"]:
                            if frame[side]["players"] is not None and (
                                len(frame[side]["players"])
                                > 0  # Used to be == 5, to ensure the sides were equal.
                            ):
                                for player in frame[side]["players"]:
                                    player_item = {}
                                    player_item["roundNum"] = r["roundNum"]
                                    player_item["tick"] = frame["tick"]
                                    player_item["seconds"] = frame["seconds"]
                                    player_item["side"] = side
                                    player_item["teamName"] = frame[side]["teamName"]
                                    for col in player.keys():
                                        if col in ["isAlive"]:
                                            player_item[col] = player[col]
                                        if col in ["inventory"]:
                                            if player[col] is not None:
                                                for item in player[col]:
                                                    if item['weaponClass'] == 'Rifle':
                                                        player_item['Rifle'] = item['weaponName']
                                                    if item['weaponClass'] == 'SMG':
                                                        player_item['SMG'] = item['weaponName']
                                                    if item['weaponClass'] == 'Heavy':
                                                        player_item['Heavy'] = item['weaponName']
                                                    if item['weaponClass'] == 'Pistols':
                                                        player_item['Pistols'] = item['weaponName']
                                                    if item['weaponName'] == 'Flashbang':
                                                        player_item['Flashbang'] = item['ammoInMagazine'] + item['ammoInReserve']
                                                    if item['weaponName'] == 'Molotov':
                                                        player_item['Molotov'] = item['ammoInMagazine']
                                                    if item['weaponName'] == 'HE Grenade':
                                                        player_item['HE'] = item['ammoInMagazine']
                                                    if item['weaponName'] == 'Smoke Grenade':
                                                        player_item['Smore'] = item['ammoInMagazine']
                                                    if item['weaponName'] == 'Decoy Grenade':
                                                        player_item['Decoy'] = item['ammoInMagazine']
                                    player_frames.append(player_item)
            player_frames_df = pd.DataFrame(player_frames)
            player_frames_df["matchID"] = self.json["matchID"]
            player_frames_df["mapName"] = self.json["mapName"]
            return pd.DataFrame(player_frames_df)
        else:
            self.logger.error(
                "JSON not found. Run .parse() or .read_json() if JSON already exists"
            )
            raise AttributeError(
                "JSON not found. Run .parse() or .read_json() if JSON already exists"
            )
# %%
demofile = os.path.join(DEMOS_DIR, "2022-03-26__0007__1__15477821__de_train__timemlopes__vs__timepurpz.dem")
demo_parser = DemoParserGC(demofile=demofile, demo_id="timemlopes__vs__timepurpz", parse_rate=128)

demo_parser.parse()
# %%
df_frames = demo_parser._parse_frames()
df_frames.head()
# %%
df_frames.columns
# %%
df_player_frames = demo_parser._parse_player_frames()
df_player_frames.head()
# %%
df_player_frames.head()
# %%
df_player_inventory_frames = demo_parser._parse_player_inventory_frames()
df_player_inventory_frames.head()
# %%
df_player_inventory_frames.columns
# %%
df_rounds = demo_parser._parse_rounds()
df_rounds.head()
# %%
df_rounds.columns
# %%
df_kills = demo_parser._parse_kills()
df_kills.head()
# %%
df_kills.columns
# %%
df_frames[['roundNum','seconds','ctEqVal','tEqVal','tAlivePlayers','ctUtility','tUtility']]
# %%
df_rounds[['roundNum','mapName','winningSide','roundEndReason']]
# %%
df_player_inventory_frames