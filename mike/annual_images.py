#%%

import geowombat as gw
from glob import glob

files = sorted(glob("/home/mmann1123/Downloads/MODIS_NDVI/*.tif"))

#%%
with gw.open(files) as src:

    print(src)
# %%
