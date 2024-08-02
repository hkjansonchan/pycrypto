import os
import ccxt
import pandas as pd
from datetime import datetime, timedelta, timezone
from tool import ifcsvempty

def fetch(csv_path, crypto = "BTC", interval = "15m", start = "2018-01-01 00:00:00"):
    style = "%Y-%m-%d %H:%M:%S"

    if os.path.isfile(csv_path) == True and ifcsvempty(csv_path) == True:
        while True:
            csv = pd.read_csv(csv_path)
            date_obj = datetime.strptime(str(csv.iloc[-1, 0]), style)
            date_obj += timedelta(minutes=15)
            ex = ccxt.binance()
            now = datetime.now(timezone.utc)
            dt_string = now.strftime(style)
            dt_string = datetime.strptime(dt_string, style)
            if date_obj <= dt_string:
                from_ts = ex.parse8601(str(date_obj))
                ohlcv_list = []
                ohlcv = ex.fetch_ohlcv(f"{crypto}/USDT", interval, since=from_ts, limit=1000)
                ohlcv_list.append(ohlcv[1:])
                # Convert ohlcv to DataFrame
                new_df = pd.DataFrame(
                    ohlcv, columns=["date", "open", "high", "low", "close", "volume"]
                )
                new_df["date"] = pd.to_datetime(new_df["date"], unit="ms")

                # Append new data to existing CSV
                csv = pd.concat([csv, new_df], ignore_index=True)
                csv.to_csv(csv_path, index=False)
            else:
                break

    else:
        if os.path.isfile(csv_path) == False:
            # Create new CSV file
            f = open(csv_path, "x")
        # Fetch new data to CSV
        ex = ccxt.binance()
        from_ts = ex.parse8601(start)
        ohlcv_list = []
        ohlcv = ex.fetch_ohlcv(f"{crypto}/USDT", interval, since=from_ts, limit=1000)
        ohlcv_list.append(ohlcv)
        while True:
            from_ts = ohlcv[-1][0]
            new_ohlcv = ex.fetch_ohlcv(f"{crypto}/USDT", interval, since=from_ts, limit=1000)
            ohlcv.extend(new_ohlcv[1:])
            if len(new_ohlcv) != 1000:
                break
        df = pd.DataFrame(ohlcv, columns=["date", "open", "high", "low", "close", "volume"])
        df["date"] = pd.to_datetime(df["date"], unit="ms")
        df.set_index("date", inplace=True)
        df = df.sort_index(ascending=True)
        df.to_csv(csv_path)

if __name__ == "__main__":
    from var import raw
    fetch(raw)
 