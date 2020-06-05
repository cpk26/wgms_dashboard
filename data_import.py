# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
import numpy as np
import os
import pyproj


# %%
data_dir = './DOI-WGMS-FoG-2019-12/'
a_glacier_file = 'WGMS-FoG-2019-12-A-GLACIER.csv'

# %%
df_combined = pd.DataFrame()

# %% [markdown]
# ### Read WGMS_A file to extract lat-long; drop rows with null values in lat-long

# %%
df_A = pd.read_csv(os.path.join(data_dir,a_glacier_file))
df_A.dropna(axis='rows',subset=['LONGITUDE','LATITUDE'], inplace=True)

# %%
wgms_projection = pyproj.Proj(init='epsg:4326')  # wgs84
web_projection = pyproj.Proj(init='epsg:3857')  # default google projection

df_combined['long'], df_combined['lat'] = df_A['LONGITUDE'], df_A['LATITUDE']
df_combined['merX'],df_combined['merY'] = pyproj.transform(wgms_projection, web_projection, df_combined['long'].values, df_combined['lat'].values)


# %%
df_combined.to_pickle('wgms_combined')

# %%
