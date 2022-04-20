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

coords_maps = [
    {
        'de_train':{
            'startX': -2500.0,
            'endX': 2345.0,
            'startY': -2420.0,
            'endY': 2390.0,
        }
    }
]


def pointx(xinput, startX, endX, resx):
    sizex = endX - startX
    if startX < 0:
        xinput += startX * -1.0
    else:
        xinput += startX
    xoutput = (xinput / abs(sizex)) * resx
    return xoutput

def pointy(yinput, startY, endY, resy):
    sizey = endY - startY
    if startY < 0:
        yinput += startY * -1.0
    else:
        yinput += startY
    youtput = (yinput / abs(sizey)) * resy
    return youtput
# %%
x_pos = pointx(df_kills['attackerX'],
       startX=coords_maps[0]['de_train']['startX'],
       endX=coords_maps[0]['de_train']['endX'],
       resx=1024,)

y_pos = pointy(df_kills['attackerY'],
       startY=coords_maps[0]['de_train']['startY'],
       endY=coords_maps[0]['de_train']['endY'],
       resy=1024,)

x_pos_v = pointx(df_kills['victimX'],
         startX=coords_maps[0]['de_train']['startX'],  
            endX=coords_maps[0]['de_train']['endX'],
            resx=1024,)

y_pos_v = pointy(df_kills['victimY'],
         startY=coords_maps[0]['de_train']['startY'],
            endY=coords_maps[0]['de_train']['endY'],
            resy=1024,)

# %%
image_file = os.path.join(MAPS_DIR, "de_train.jpg")
img = plt.imread(image_file)
fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(img, extent=[0, 1024, 0, 1024])
ax.plot(x_pos, y_pos, 'bo', alpha=0.5)

ax.plot(x_pos_v, y_pos_v, 'ro', alpha=0.5)

plt.show()
# %%
df_processed = pd.DataFrame(data={'x_atk': x_pos, 'y_atk': y_pos, 'x_victim': x_pos_v, 'y_victim': y_pos_v, 'name': df_kills['attackerName'], 'side': df_kills['attackerSide']})

# '★ ⑮ batata', '★ ⑭ LioN', '★ ⑭ Xilanta', '★ ⑩ Roger do Roger That', '★ ④ Coelho', '★ ④ mlopes', '★ ⑭ purpz', '★ ⑥ chellesChelles', '★ ⑭ Campeiro', '★ ③ TeoMeWhy'
nick = '★ ③ TeoMeWhy'
# 'T', 'CT'
side = 'CT'

df_transformed = df_processed[(df_processed['side'] == side) & (df_processed['name'] == nick)]

image_file = os.path.join(MAPS_DIR, "de_train.jpg")
img = plt.imread(image_file)
fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(img, extent=[0, 1024, 0, 1024])

for i in df_transformed.values:
    ax.plot([i[0], i[2]], [i[1], i[3]], marker='+', color='r', alpha=0.3)

ax.plot(df_transformed['x_atk'], df_transformed['y_atk'], '+', color='b', alpha=0.9)
ax.plot(df_transformed['x_victim'], df_transformed['y_victim'], '+', color='r', alpha=0.9)

plt.show()
# %%

# %%

# %%
