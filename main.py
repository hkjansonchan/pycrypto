from discord import discord_send
from fetch import fetch
from analysis import analysis


# Run fetch.py
fetch()

# Run analysis.py
df = analysis()

print(df.iloc[-1, -1])
# Run discord.py
# discord_send("")
