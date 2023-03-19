import pandas as pd


def format_df(df: pd.DataFrame, select_team: int, drop_team: int) -> pd.DataFrame:
    df = df.drop(columns=[f"spi{drop_team}", f"prob{drop_team}"])

    df = df.rename(
        columns={
            f"team{select_team}": "team", 
            f"spi{select_team}": "spi", 
            f"prob{select_team}": "prob", 
            f"team{drop_team}": "adversary",
            f"score{select_team}": "score",
            f"score{drop_team}": "score_adversary"
        })

    return df
    

df = pd.read_csv("pratices/pratice_4/data/VIS_Pr04_worldcup_matches.csv")

df_team1 = format_df(df, 1, 2)
df_team2 = format_df(df, 2, 1)

result_df = pd.concat([df_team1, df_team2])

result_df.to_csv("pratices/pratice_4/output_data/selections_metrics.csv")
