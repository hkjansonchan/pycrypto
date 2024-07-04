import pandas as pd


def cut_df(data: pd.DataFrame, start_date: str, set_index: str = False):
    data["date"] = pd.to_datetime(data["date"])
    if set_index:
        data = data.set_index(set_index)
    data_slice = data.loc[start_date:]
    return data_slice


if __name__ == "__main__":
    df = cut_df(pd.read_csv("btc15m.csv"), "2024-06-01")
    df.to_csv("clip15m.csv")
