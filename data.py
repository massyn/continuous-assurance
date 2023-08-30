import pandas as pd

DATALAKE = '_datalake'

df = pd.read_csv(f"{DATALAKE}/rollup.csv")
df["datestamp"] = pd.to_datetime(df["datestamp"],format="%Y-%m-%d")

df_detail = pd.read_csv(f"{DATALAKE}/detail.csv")
df_detail["datestamp"] = pd.to_datetime(df_detail["datestamp"],format="%Y-%m-%d")