import pandas as pd
import talib
from tool import cut_df, time_arithmetic as t_a

# path = "btc15m.csv"
start_d = "2024-07-01"  # Start date


def analyze_data(data_path: str, start_date: str = False):
    # Read data from CSV assuming columns are named 'open', 'high', 'low', 'close', 'volume'
    df = pd.read_csv(data_path)
    if start_date:
        df = cut_df(pd.read_csv(data_path), start_date)

    # Calculate MACD
    macd, macdsignal, macdhist = talib.MACD(
        df["close"], fastperiod=12, slowperiod=26, signalperiod=9
    )

    # Add MACD columns
    df["macd"] = macd
    df["macdsignal"] = macdsignal
    df["macdhist"] = macdhist

    # Calculate RSI
    df["rsi"] = talib.RSI(df["close"], timeperiod=14)

    # Calculate Bollinger Bands
    upperband, middleband, lowerband = talib.BBANDS(
        df["close"], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
    )
    df["upperband"] = upperband
    df["middleband"] = middleband
    df["lowerband"] = lowerband

    # Calculate Stochastic Oscillator (%K, %D)
    k, d = talib.STOCH(
        df["high"],
        df["low"],
        df["close"],
        fastk_period=5,
        slowk_period=3,
        slowd_period=3,
    )
    df["k"] = k
    df["d"] = d

    # Volume analysis (basic example)
    df["volume_change"] = df["volume"].diff()  # Change in volume

    # Simple bullish/bearish signal based on MACD crossover (Not a trading strategy)
    df["macd_signal"] = ""
    for i in range(len(df)):
        if df.loc[i, "macd"] > df.loc[i, "macdsignal"]:
            df.loc[i, "macd_signal"] = "Bullish"
        elif df.loc[i, "macd"] < df.loc[i, "macdsignal"]:
            df.loc[i, "signal"] = "Bearish"

    # Additional analysis based on RSI, Bollinger Bands, Stochastic, and Volume (for illustration)
    df["signal"] = ""
    for i in range(len(df)):
        if df.loc[i, "macd_signal"] == "Bullish" and df.loc[i, "rsi"] < 70:
            df.loc[i, "signal"] = "Strong Buy"
        elif df.loc[i, "macd_signal"] == "Bearish" and df.loc[i, "rsi"] > 70:
            df.loc[i, "signal"] = "Strong Sell"
        elif df.loc[i, "close"] > df.loc[i, "upperband"]:
            df.loc[i, "signal"] = "Potential Overbought"
        elif df.loc[i, "close"] < df.loc[i, "lowerband"]:
            df.loc[i, "signal"] = "Potential Oversold"
        elif df.loc[i, "k"] > 80 and df.loc[i, "d"] > 80:
            df.loc[i, "signal"] = "Potential Overbought (Stochastic)"
        elif df.loc[i, "k"] < 20 and df.loc[i, "d"] < 20:
            df.loc[i, "signal"] = "Potential Oversold (Stochastic)"
        elif df.loc[i, "volume_change"] > 0 and df.loc[i, "macd_signal"] == "Bullish":
            df.loc[i, "signal"] = "Bullish Volume Confirmation"
        elif df.loc[i, "volume_change"] < 0 and df.loc[i, "macd_signal"] == "Bearish":
            df.loc[i, "signal"] = "Bearish Volume Confirmation"

    return df


def analysis(raw, ana):  # main()
    df = pd.read_csv(ana)
    start_date = t_a(df.iloc[-1, 0], operation="-", minutes=15 * 40)
    df = pd.concat(
        [df, cut_df(analyze_data(raw, start_date), t_a(df.iloc[-1, 0], minutes=15))],
        ignore_index=True,
        sort=False,
    )
    df.to_csv(ana, index=False)
    ls = df.iloc[-2:, [0, -2, -1]].values.tolist()
    ls.insert(0, [df.columns[0], df.columns[-2], df.columns[-1]])
    temp = []
    p = []
    for i in ls:
        temp.append([str(j) for j in i])
    r = f"{temp[0][0]}\t\t\t\t\t{temp[0][1]}\t\t{temp[0][2]}\n{temp[1][0]}\t\t{temp[1][1]}\t\t\t\t{temp[1][2]}\n{temp[2][0]}\t\t{temp[2][1]}\t\t\t\t{temp[2][2]}"
    return r


if __name__ == "__main__":
    """
    df = analyze_data(path, start_date=False)
    """
    print(analysis())
