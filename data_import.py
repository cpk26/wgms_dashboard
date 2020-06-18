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
d_change_file = 'WGMS-FoG-2019-12-D-CHANGE.csv'
ee_massbalance_file =  'WGMS-FoG-2019-12-EE-MASS-BALANCE.csv'
c_front_file = 'WGMS-FoG-2019-12-C-FRONT-VARIATION.csv'

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
# ### Time Series

# %%
def ts_helper(df, columns):
    #One measurement per Year
    df_median = df.loc[:,columns].groupby(columns[0:2], as_index=False).median()
    
    #Add Zero 2020 measurement so that no group has less than two entries
    duplicates = df['WGMS_ID'].duplicated(keep=False)
    single_year_ids = df.loc[~duplicates,'WGMS_ID']

    zero_frame = pd.DataFrame([[wid, 2020, 0] for wid in single_year_ids], columns=columns)
    df_out = df_median.append(zero_frame)
    return df_out


# %% [markdown]
# ### Thickness Change

# %%
df_D = pd.read_csv(os.path.join(data_dir,d_change_file))
df_D.dropna(axis='rows',subset=['THICKNESS_CHG'], inplace=True)

# %%

D_columns = ['WGMS_ID','YEAR','THICKNESS_CHG']
df_thickness_chg = ts_helper(df_D,D_columns)

# %% [markdown]
# ### Mass Balance

# %%
df_EE = pd.read_csv(os.path.join(data_dir,ee_massbalance_file))
df_EE.dropna(axis='rows',subset=['ANNUAL_BALANCE'], inplace=True)

EE_columns=['WGMS_ID','YEAR','ANNUAL_BALANCE']
df_mass_balance = ts_helper(df_EE,EE_columns)

# %% [markdown]
# ### Length 

# %%
df_C = pd.read_csv(os.path.join(data_dir,c_front_file))
df_C.columns = df_C.columns.str.upper()
df_C.dropna(axis='rows',subset=['FRONT_VARIATION'], inplace=True)

C_columns=['WGMS_ID','YEAR','FRONT_VARIATION']
df_front = ts_helper(df_C,C_columns)

# %% [markdown]
# ### Save File and Print out Leading lines

# %%
df_compiled.to_pickle('wgms_combined')
df_thickness_chg.to_pickle('wgms_thickness')
df_mass_balance.to_pickle('wgms_massbalance')
df_front.to_pickle('wgms_front')

# %%

# %%
df_compiled.head(n=2)

# %%
df_thickness_chg.query('WGMS_ID == 4630')

# %%
df_compiled[df_compiled['NAME'].str.contains('glace', case=False)]

# %%
