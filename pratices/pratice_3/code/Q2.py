import pandas as pd

def format_df(df: pd.DataFrame, year: int) -> pd.DataFrame:
    df = (
        df[["Country", str(year)]]
        .rename(columns={str(year): "hunger_index"})
    )
    df["hunger_index"] = df["hunger_index"].str.replace("<", "", regex=True)
    df["year"] = year
    
    return df

df = pd.read_csv("pratices/pratice_3/data/VIS_Pr_03_hungry_in_the_world.csv")


df_chances = df[["Country", "Absolute change since 2014", "Percent change sice 2014"]].set_index("Country")

df_2000 = format_df(df, 2000)
df_2007 = format_df(df, 2007)
df_2014 = format_df(df, 2014)
df_2022 = format_df(df, 2022)

concat_df = (
    pd.concat(
        [df_2000, df_2007, df_2014, df_2022]
        )
        .set_index("Country")
)
df_chances.to_csv("pratices/pratice_3/output_data/chances.csv")
concat_df.to_csv("pratices/pratice_3/output_data/ghi.csv")