import pandas as pd


def cut_df(data: pd.DataFrame, start_date: str, set_index: str = False):
    data["date"] = pd.to_datetime(data["date"])
    if set_index:
        data = data.set_index(set_index)
    start_date = pd.to_datetime(start_date)
    df = data[data["date"] >= start_date]
    df = df.reset_index()
    df = df.iloc[:, 1:]
    #df.set_index("date", inplace=True)
    return df


if __name__ == "__main__":
    df = cut_df(pd.read_csv("btc15m.csv"), "2024-06-01")
    print(df)
