import pandas as pd
import talib
from tool import cut_df


def analyze_bitcoin_data(data_path: str, start_date: str):
    # Read data from CSV assuming columns are named 'open', 'high', 'low', 'close', 'volume'
    df = pd.read_csv(data_path)
    df = cut_df(df, start_date)

    # Calculate MACD
    macd, macdsignal, macdhist = talib.MACD(
        df["close"], fastperiod=12, slowperiod=26, signalperiod=9
    )

    # Add MACD columns
    df["macd"] = macd
    df["macdsignal"] = macdsignal
    df["macdhist"] = macdhist

    # Calculate RSI (Relative Strength Index)
    df["rsi"] = talib.RSI(df["close"], timeperiod=14)

    # Calculate Bollinger Bands (BBANDS)
    upperband, middleband, lowerband = talib.BBANDS(
        df["close"], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
    )
    df["upperband"] = upperband
    df["middleband"] = middleband
    df["lowerband"] = lowerband

    # Simple bullish/bearish signal based on MACD crossover (Not a trading strategy)
    df["macd_signal"] = ""
    for i in range(len(df)):
        if df.loc[i, "macd"] > df.loc[i, "macdsignal"]:
            df.loc[i, "macd_signal"] = "Bullish"
        elif df.loc[i, "macd"] < df.loc[i, "macdsignal"]:
            df.loc[i, "macd_signal"] = "Bearish"

    # Additional analysis based on RSI and Bollinger Bands (for illustration)
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

    return df


def analyze_bitcoin_data2(df):
    # Read data from CSV assuming columns are named 'open', 'high', 'low', 'close', 'volume'
    #df = pd.read_csv(data_path)
    #df = cut_df(pd.read_csv(data_path), "2024-06-01")
    
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


data_path = "btc15m.csv"
start_date = "2024-06-01"
df = analyze_bitcoin_data2(pd.read_csv(data_path))

print(df)
#df.to_csv("analysis.csv")
#print(cut_df(pd.read_csv(data_path), "2024-06-01"))