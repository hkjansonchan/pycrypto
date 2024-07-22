import pandas as pd
import talib
from tool import cut_df, find_in_first_column as find, time_arithmetic as t_a
import os
from datetime import datetime, timedelta, timezone
from fetch import ifcsvempty
import ccxt

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


def analyze_bitcoin_data2(data_path: str, start_date: str):
    # Read data from CSV assuming columns are named 'open', 'high', 'low', 'close', 'volume'
    df = pd.read_csv(data_path)
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


def test():
    data_1 = {'name':['Alan','Joseph','Wennie', 'Ruby'],
            'gender':['M','M','F','F'],
            'city':['Taipei','Hualien','Hsinchu', 'Taoyuan']}
    data_2 = {'name':['Ruby','Chris','Tanya'],
            'gender':['F','M','F'],
            'city':['Taoyuan','Kaohsiung', 'Taichung']}
    df1 = pd.DataFrame(data_1)
    df2 = pd.DataFrame(data_2)
    print('data_1')
    print(df1)
    print('data_2')
    print(df2)
    con = pd.concat([df1,df2],ignore_index=True)
    print('concat')
    print(con)
    df = pd.concat([df1,df2],ignore_index=True).drop_duplicates()
    print('concat with .drop_duplicates()')
    print(df)
    print(find(df,'Joseph'))


######################################################################################
raw = "/home/hkjansonchan/pycrypto/btc15m.csv"
ana = "/home/hkjansonchan/pycrypto/analysis_btc.csv"
from analysis import analyze_data

if ifcsvempty(ana):
    ana_df = pd.read_csv(ana)
    ana_last_date = str(ana_df.iloc[-1, 0]) # -1 for last row, 0 for first column
    start_date = datetime.strptime(ana_last_date, "%Y-%m-%d %H:%M:%S") + timedelta(minutes=40*15)
    print(start_date)
    new_df = analyze_data(raw, start_date)
    new_df = new_df[36:]
    first_date = new_df.iloc[0, 0]
    ana_index = ana_df[ana_df.iloc[:, 0]==str(first_date)].index[0]
    df = pd.concat([ana_df[:ana_index], new_df], ignore_index=True)
