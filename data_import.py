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
import string


# %%
# Data Directory
data_dir = "./DOI-WGMS-FoG-2019-12/"

# WGMS Data Files
a_glacier_file = "WGMS-FoG-2019-12-A-GLACIER.csv"
b_glacier_file = "WGMS-FoG-2019-12-B-STATE.csv"
d_change_file = "WGMS-FoG-2019-12-D-CHANGE.csv"
e_massbalance_file = "WGMS-FoG-2019-12-E-MASS-BALANCE-OVERVIEW.csv"
ee_massbalance_file = "WGMS-FoG-2019-12-EE-MASS-BALANCE.csv"
c_front_file = "WGMS-FoG-2019-12-C-FRONT-VARIATION.csv"

# %%
# Main dataframe containing overall information
df_compiled = pd.DataFrame()

# %% [markdown]
# ### Extract relevant Glacial Characteristics from the WGMS_A file

# %%
df_A = pd.read_csv(os.path.join(data_dir, a_glacier_file))
df_A.dropna(axis="rows", subset=["LONGITUDE", "LATITUDE"], inplace=True)

# %%
df_A.columns

# %%
# Extract relevant columns
A_columns = [
    "WGMS_ID",
    "LONGITUDE",
    "LATITUDE",
    "POLITICAL_UNIT",
    "GLACIER_REGION_CODE",
    "SPEC_LOCATION",
    "NAME",
    "PRIM_CLASSIFIC",
    "FORM",
    "FRONTAL_CHARS",
    "EXPOS_ACC_AREA",
    "EXPOS_ABL_AREA",
    "REMARKS",
]

df_A['NAME'] = df_A['NAME'].apply(lambda x: string.capwords(x))

notna = df_A['SPEC_LOCATION'].notna()
df_A.loc[notna,'SPEC_LOCATION'] = df_A.loc[notna,'SPEC_LOCATION'].apply(lambda x: string.capwords(str(x)))

df_compiled = df_A.loc[:, A_columns]


# %%
# Mercator X and Y coordinates
transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
df_compiled.loc[:, "merX"], df_compiled.loc[:, "merY"] = transformer.transform(
    df_compiled["LONGITUDE"].values, df_compiled["LATITUDE"].values
)

# %% [markdown]
# ### Extract additional data from WGMS_B File

# %%
df_B = pd.read_csv(os.path.join(data_dir, b_glacier_file))
df_B.columns

# %%
df_B_reduced = df_B.loc[
    :,
    [
        "WGMS_ID",
        "YEAR",
        "HIGHEST_ELEVATION",
        "LOWEST_ELEVATION",
        "INVESTIGATOR",
        "SPONS_AGENCY",
        "REFERENCE",
    ],
]
df_B_reduced.drop_duplicates("WGMS_ID", keep="last", inplace=True)


# %% [markdown]
# ### Time Series

# %% [markdown]
# Create time series for the following data:
# 1. Thickness Change
# 2. Mass Balance
# 3. Length

# %%
def ts_helper(df, columns):
    """Extract time series data so that: 
        1: There is one measurement per year; multiple measurements are summarized crudely with median()
        2: Add a measurement in 2020, with value zero, for plotting purposes
        """

    # One measurement per Year
    df_median = df.loc[:, columns].groupby(columns[0:2], as_index=False).median()
    df_out = df_median

    return df_out


# %% [markdown]
# ### Thickness and Area Change

# %%
df_D = pd.read_csv(os.path.join(data_dir, d_change_file))
df_th = df_D.copy()
df_ar = df_D.copy()

# %%
df_D.columns

# %%
df_th.dropna(axis="rows", subset=["THICKNESS_CHG"], inplace=True)
th_columns = ["WGMS_ID", "YEAR", "THICKNESS_CHG"]
df_thickness_chg = ts_helper(df_th, th_columns)

# %% [markdown]
# ### Area Change

# %%
df_ar.dropna(axis="rows", subset=["AREA_CHANGE"], inplace=True)

# %%
ar_columns = ["WGMS_ID", "YEAR", "AREA_CHANGE"]
df_area_chg = ts_helper(df_ar, ar_columns)

# %%
df_area_chg

# %% [markdown]
# ### Mass Balance

# %%
df_EE = pd.read_csv(os.path.join(data_dir, ee_massbalance_file))
df_EE.dropna(axis="rows", subset=["ANNUAL_BALANCE"], inplace=True)

EE_columns = ["WGMS_ID", "YEAR", "ANNUAL_BALANCE"]
df_mass_balance = ts_helper(df_EE, EE_columns)

# %% [markdown]
# ### Length

# %%
df_C = pd.read_csv(os.path.join(data_dir, c_front_file))
df_C.columns = df_C.columns.str.upper()
df_C.dropna(axis="rows", subset=["FRONT_VARIATION"], inplace=True)

C_columns = ["WGMS_ID", "YEAR", "FRONT_VARIATION"]
df_front = ts_helper(df_C, C_columns)

# %% [markdown]
# ### Extract site Time Series Characteristics

# %%
df_wgms = df_compiled.loc[:, ["WGMS_ID"]]

# %% [markdown]
# ### First Measurement

# %%
dfs = [
    df.loc[:, ["WGMS_ID", "YEAR"]].set_index("WGMS_ID")
    for df in [df_thickness_chg, df_mass_balance, df_front]
]
dfs_ = [df.groupby("WGMS_ID")["YEAR"].min() for df in dfs]
df_first_measurement = pd.concat(dfs_, axis=1, join="outer").min(axis=1).reset_index()
df_first_measurement.rename({0: "FIRST_MEAS"}, axis=1, inplace=True)

# %% [markdown]
# ### Years of Measurements

# %%
dfs = [
    df.loc[:, ["WGMS_ID", "YEAR"]]
    for df in [df_thickness_chg, df_mass_balance, df_front]
]
dfs_ = pd.concat(dfs).drop_duplicates(keep="first")
df_year_measurement = dfs_.groupby("WGMS_ID").size().reset_index()
df_year_measurement.rename({0: "YEAR_MEASUREMENTS"}, axis=1, inplace=True)

# %% [markdown]
# ### Concatenate

# %%
df_compiled = df_compiled.merge(df_B_reduced, how="left", on="WGMS_ID", validate="1:1")
df_compiled = df_compiled.merge(df_first_measurement, on="WGMS_ID", how="left")
df_compiled = df_compiled.merge(df_year_measurement, on="WGMS_ID", how="left")

# Set first measurement to 2020 if value is Nan, measured years to zero if value is NaN
df_compiled.replace(
    {
        "FIRST_MEAS": {np.nan: 2020},
        "YEAR_MEASUREMENTS": {np.nan: 0},
        "PRIM_CLASSIFIC": {np.nan: 10},
        "FORM": {np.nan: 10},
        "FRONTAL_CHARS": {np.nan: 10},
        "SPEC_LOCATION": {np.nan: "N/A"},
        "NAME": {np.nan: "N/A"},
        "INVESTIGATOR": {np.nan: "N/A"},
        "SPONS_AGENCY": {np.nan: "N/A"},
        "REMARKS": {np.nan: "N/A"},
        "REFERENCE": {np.nan: "N/A"},

    },
    inplace=True,
)

# %%
df_compiled.head(n=10)

# %% [markdown]
# ### Save Files

# %%
df_compiled.to_pickle("wgms_combined")
df_thickness_chg.to_pickle("wgms_thickness")
df_mass_balance.to_pickle("wgms_massbalance")
df_front.to_pickle("wgms_front")

# %% [markdown]
# ### WGMS ID of MER DE GLACE

# %%
df_compiled[df_compiled["NAME"].str.contains("glace", case=False)]

# %%
df_compiled.query("WGMS_ID == 353")

# %%
df_compiled['HIGHEST_ELEVATION'][0] is np.nan

# %%

