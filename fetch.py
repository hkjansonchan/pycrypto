import ccxt
import pandas as pd

ex = ccxt.binance()
from_ts = ex.parse8601('2018-01-01 00:00:00')
ohlcv_list = []
ohlcv = ex.fetch_ohlcv('BTC/USDT', '15m', since=from_ts, limit=1000)
ohlcv_list.append(ohlcv)
while True:
  from_ts = ohlcv[-1][0]
  new_ohlcv = ex.fetch_ohlcv('BTC/USDT', '15m', since=from_ts, limit=1000)
  ohlcv.extend(new_ohlcv)
  if len(new_ohlcv) != 1000:
    break

df = pd.DataFrame(ohlcv, columns=['date', 'open', 'high', 'low', 'close', 'volume']) # type: ignore
df['date'] = pd.to_datetime(df['date'], unit='ms')
df.set_index('date', inplace=True)
df = df.sort_index(ascending=True)
df.head()
df.to_csv("data.csv")