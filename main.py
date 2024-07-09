from discord import discord_send
from fetch import fetch
from analysis import analysis


# Run fetch.py
fetch()

# Run analysis.py
mes = analysis()

# Run discord.py
discord_send(mes)
