import os
import ccxt
import pandas as pd
from datetime import datetime, timedelta


def ifcsvempty(path: str):
    try:
        pd.read_csv(path)
        return True
    except:
        return False


if os.path.isfile("data.csv") == True and ifcsvempty("data.csv"):
    # Fetch to last row
    csv = pd.read_csv("data.csv")
    date_obj = datetime.strptime(csv.iloc[-1, 0], "%Y-%m-%d %H:%M:%S")
    date_obj += timedelta(minutes=15)
    ex = ccxt.binance()
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    dt_string = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
    if date_obj <= dt_string:
        from_ts = ex.parse8601(str(date_obj))
        ohlcv_list = []
        ohlcv = ex.fetch_ohlcv("BTC/USDT", "15m", since=from_ts, limit=None)
        ohlcv_list.append(ohlcv)
        # Convert ohlcv to DataFrame
        new_df = pd.DataFrame(ohlcv, columns=["date", "open", "high", "low", "close", "volume"])
        new_df["date"] = pd.to_datetime(new_df["date"], unit="ms")

        # Append new data to existing CSV
        csv = pd.concat([csv, new_df], ignore_index=True)
        csv.to_csv("data.csv", index=False)
    else:
        pass

else:
    if os.path.isfile("data.csv") == False:
        # Create new CSV file
        f = open("data.csv", "x")
    # Fetch new data to CSV
    ex = ccxt.binance()
    from_ts = ex.parse8601("2018-01-01 00:00:00")
    ohlcv_list = []
    ohlcv = ex.fetch_ohlcv("BTC/USDT", "15m", since=from_ts, limit=1000)
    ohlcv_list.append(ohlcv)
    while True:
        from_ts = ohlcv[-1][0]
        new_ohlcv = ex.fetch_ohlcv("BTC/USDT", "15m", since=from_ts, limit=1000)
        ohlcv.extend(new_ohlcv)
        if len(new_ohlcv) != 1000:
            break

    df = pd.DataFrame(ohlcv, columns=["date", "open", "high", "low", "close", "volume"])
    df["date"] = pd.to_datetime(df["date"], unit="ms")
    df.set_index("date", inplace=True)
    df = df.sort_index(ascending=True)
    df.head()
    df.to_csv("data.csv")
