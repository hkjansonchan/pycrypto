from discord_webhook import DiscordWebhook

webhook_url = "https://discordapp.com/api/webhooks/1259877682905088145/smMP42MO47H4n3TQhgAsVLvWRmF5LLPA8nYnajsZT0erzzAIPxzLOhsXW21VgE3eCRn8"


def discord_send(mes: str):
    webhook = DiscordWebhook(url=webhook_url, content=mes)
    webhook.execute()

if __name__ == "__main__":
    discord_send("Hello, World!")
