import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
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

