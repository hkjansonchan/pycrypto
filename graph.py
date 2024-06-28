import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf


def graph(file: str, start_date: str):
    data = pd.read_csv(file)
    data["date"] = pd.to_datetime(data["date"])
    data = data.set_index("date")
    data_slice = data.loc[start_date:]
    mpf.plot(data_slice[["open", "high", "low", "close"]], type="line")


if __name__ == "__main__":
    graph("btc15m.csv", "2024-06-01")
