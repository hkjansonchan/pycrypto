import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential  # type: ignore
from keras.layers import Dense, LSTM, Dropout, Input  # type: ignore
from discord_webhook import DiscordWebhook


def dcsend(url: str, mes: str):
    webhook = DiscordWebhook(url=url, content=mes)
    webhook.execute()


webhook_url = ""

# Run fetch.py
try:
    os.system("fetch.py")
except Exception as e:
    print(f"Error: {e}")
