# %%
from src.core.scrap import ScrapHLTV
import numpy as np
# %%
offsets = np.linspace(0,500,6,dtype=int)
# %%
for offset in offsets:
    scrap = ScrapHLTV(offset=offset).start()
# %%
