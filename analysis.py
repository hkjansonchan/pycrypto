import pandas as pd
import talib
from datetime import datetime, timedelta
from tool import cut_df, ifcsvempty, time_arithmetic as t_a, find_in_first_column as find


start_d = "2024-07-01"  # Start date
raw = "/home/hkjansonchan/pycrypto/btc15m.csv"
ana = "/home/hkjansonchan/pycrypto/analysis_btc.csv"


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
    if ifcsvempty(ana):
        ana_df = pd.read_csv(ana)
        ana_last_date = str(ana_df.iloc[-1, 0]) # -1 for last row, 0 for first column
        start_date = datetime.strptime(ana_last_date, "%Y-%m-%d %H:%M:%S") - timedelta(minutes=40*15)
        new_df = analyze_data(raw, start_date)
        new_df = new_df[36:]
        first_date = new_df.iloc[0, 0] # analyzed data first date
        ana_index = ana_df[ana_df.iloc[:, 0]==str(first_date)].index[0]
        df = pd.concat([ana_df[:ana_index], new_df], ignore_index=True)
    else:
        df = analyze_data(raw)
    
    df.to_csv(ana, index=False)
    l = df.iloc[-2:, [0, -2, -1]].reset_index(drop=True).values.tolist()
    if l[0][1]==l[0][2]==l[1][1]==l[1][2]=='':
        return False
    else:
        mes = f'{l[0][0]}\t{l[0][1]}\t{l[0][2]}\n{l[1][0]}\t{l[1][1]}\t{l[1][2]}'
        return mes

if __name__ == "__main__":
    print(analysis(raw=raw, ana=ana))
