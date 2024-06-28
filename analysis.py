import pandas as pd
import talib as ta
import pandas_ta as pt

import matplotlib.pyplot as plt
path = "btc15m.csv"


def macd(file: str, start_date: str):
    df = pd.read_csv(file)
    macd_df = pt.macd(df["close"])
    macd_df = pd.concat([df.date, macd_df], axis=1)
    macd_df["date"] = pd.to_datetime(macd_df["date"])
    macd_df = macd_df.set_index("date")
    macd_df = macd_df.loc[start_date:]
    return macd_df


if __name__ == "__main__":
    plt.plot(macd(path, "2024-01-01").index, macd(path, "2024-01-01").MACD_12_26_9, "b", label="DIF")
    plt.show()