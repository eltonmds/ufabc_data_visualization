import yfinance as yf
from datetime import date, timedelta
from functools import reduce
import pandas as pd
from typing import List


def download_data(date_to_download: date) -> bool:
    df = yf.download("OXY", start=str(date_to_download), end=str(date_to_download + timedelta(days=1)))
    if  len(df.index) == 1:
        return df
    else:
        return download_data(date_to_download + timedelta(days=1))
    
def select_dates(amount_of_days: int, end_date: date) -> filter:
    range_days = range(amount_of_days)
    last_2500_days = map(lambda day: date.today() - timedelta(day), range_days)

    return filter(lambda day: day.day==1, last_2500_days)

    
def create_days_dfs(dates_to_download: List[date]) -> map:
    return map(lambda day: download_data(day), dates_to_download)

def aggregate_days_dfs(days_dfs: map) -> pd.DataFrame:
    return reduce(lambda acc, df: pd.concat([acc, df]), days_dfs)
        

def main() -> None:
    amount_of_days = 2500
    end_date = date.today()

    dates_to_download = select_dates(amount_of_days, end_date)
    days_dfs = create_days_dfs(dates_to_download)

    final_df = aggregate_days_dfs(days_dfs)

    final_df.to_csv("pratices/pratice_5/output_data/oxy_cotation.csv")


if __name__ == "__main__":
    main()
