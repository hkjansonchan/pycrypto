import pandas as pd
from datetime import datetime, timedelta


def cut_df(data: pd.DataFrame, start_date: str, set_index: str = False):
    data["date"] = pd.to_datetime(data["date"])
    if set_index:
        data = data.set_index(set_index)
    start_date = pd.to_datetime(start_date)
    df = data[data["date"] >= start_date]
    df = df.reset_index()
    df = df.iloc[:, 1:]
    # df.set_index("date", inplace=True)
    return df


def time_arithmetic(
    time: str,
    style: str = "%Y-%m-%d %H:%M:%S",
    operation: str = "+",
    days=0,
    seconds=0,
    microseconds=0,
    milliseconds=0,
    minutes=0,
    hours=0,
    weeks=0,
):
    match operation:
        case "+":
            date = datetime.strptime(time, style) + timedelta(
                days=days,
                seconds=seconds,
                microseconds=microseconds,
                milliseconds=milliseconds,
                minutes=minutes,
                hours=hours,
                weeks=weeks,
            )
        case "-":
            date = datetime.strptime(time, style) - timedelta(
                days=days,
                seconds=seconds,
                microseconds=microseconds,
                milliseconds=milliseconds,
                minutes=minutes,
                hours=hours,
                weeks=weeks,
            )

    return date


if __name__ == "__main__":
    df = cut_df(pd.read_csv("pycrypto/btc15m.csv"), "2024-06-01 00:14:00")
    print(df)
    #print(time_arithmetic("2024-02-29 00:00:00", operation="-", minutes=15))
    pass
