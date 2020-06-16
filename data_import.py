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
from pyproj import Transformer



# %%
data_dir = './DOI-WGMS-FoG-2019-12/'
a_glacier_file = 'WGMS-FoG-2019-12-A-GLACIER.csv'
change_glacier_file = 'WGMS-FoG-2019-12-D-CHANGE.csv'

# %%
df_compiled = pd.DataFrame()

# %% [markdown]
# ### Extract relevant Glacial Characteristics from the WGMS_A file

# %%
df_A = pd.read_csv(os.path.join(data_dir,a_glacier_file))
df_A.dropna(axis='rows',subset=['LONGITUDE','LATITUDE'], inplace=True)

# %%
df_A.columns

# %%
A_columns = ['WGMS_ID','LONGITUDE','LATITUDE','SPEC_LOCATION','NAME']
df_compiled = df_A.loc[:,A_columns]


# %%
transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
df_compiled.loc[:, 'merX'],df_compiled.loc[:, 'merY'] =transformer.transform(df_compiled['LONGITUDE'].values, df_compiled['LATITUDE'].values)

# %% [markdown]
# ### Thickness Change

# %%
df_D = pd.read_csv(os.path.join(data_dir,change_glacier_file))
df_D.dropna(axis='rows',subset=['THICKNESS_CHG'], inplace=True)

# %%
df_D['YEAR']

# %%
D_columns = ['WGMS_ID','YEAR','THICKNESS_CHG']
df_thickness_chg = df_D.loc[:,D_columns].groupby(['WGMS_ID','YEAR'], as_index=False).median()

# %%
df_thickness_chg['WGMS_ID'].nunique()

# %% [markdown]
# ### Save File and Print out Leading lines

# %%
df_compiled.to_pickle('wgms_combined')

# %%
df_compiled.head(n=2)

# %%
df_thickness_chg.to_pickle('wgms_thickness')

# %%
df_thickness_chg.head(n=2)

# %%
