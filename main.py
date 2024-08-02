import traceback
from analysis import analysis
from discord import discord_send
from fetch import fetch
from datetime import datetime
from var import (raw_data_15m as raw,
                 analysis_15m as ana,
                 webhook_url as url)


try:
    # Run fetch.py
    fetch(raw)

    # Run analysis.py
    mes = analysis(raw=raw, ana=ana)
    if mes:
        # Run discord.py
        discord_send(mes, url = url)
except:
    now = datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S"))
    traceback.print_exc()
