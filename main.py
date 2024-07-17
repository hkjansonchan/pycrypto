from discord import discord_send
from fetch import fetch
from analysis import analysis

webhook_url = ""
raw = "btc15m.csv"
ana = "analysis_btc.csv"

# Run fetch.py
fetch(raw)

# Run analysis.py
mes = analysis(raw=raw, ana=ana)

# Run discord.py
discord_send(mes, url = webhook_url)
