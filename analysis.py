import pandas as pd
import pandas_ta as pt

import matplotlib.pyplot as plt

path = "btc15m.csv"
st_da = "2024-07-01"  # Start date


def macd(file: str, start_date: str):
    df = pd.read_csv(file)
    macd_df = pt.macd(df["close"])
    macd_df = pd.concat([df.date, macd_df], axis=1)
    macd_df["date"] = pd.to_datetime(macd_df["date"])
    macd_df = macd_df.set_index("date")
    macd_df = macd_df.loc[start_date:]
    return macd_df


if __name__ == "__main__":
    plt.plot(macd(path, st_da).index, macd(path, st_da).MACD_12_26_9, "b", label="DIF")
    plt.plot(macd(path, st_da).index, macd(path, st_da).MACDs_12_26_9, "r", label="DEA")
    plt.legend()
    plt.show()