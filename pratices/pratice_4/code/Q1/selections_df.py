import pandas as pd


def format_df(df: pd.DataFrame, select_team: int, drop_team: int) -> pd.DataFrame:
    df = df.drop(columns=[f"SPI{drop_team}", f"Prob{drop_team}"])

    df = df.rename(columns={f"Team_{select_team}": "Team", f"SPI{select_team}": "SPI", f"Prob{select_team}": "Prob", f"Team_{drop_team}": "adversary"})

    return df
    

df = pd.read_csv("pratices/pratice_4/data/VIS_Pr04_worldcup_matches.csv")

df_team1 = format_df(df, 1, 2)
df_team2 = format_df(df, 2, 1)

result_df = pd.concat([df_team1, df_team2])

df.info()