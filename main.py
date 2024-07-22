import traceback
from analysis import analysis
from discord import discord_send
from fetch import fetch
from datetime import datetime


webhook_url = ""
raw = ""
ana = ""


try:
    # Run fetch.py
    fetch(raw)

    # Run analysis.py
    mes = analysis(raw=raw, ana=ana)
    if mes:
        # Run discord.py
        discord_send(mes, url = webhook_url)
except:
    now = datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S"))
    traceback.print_exc()
