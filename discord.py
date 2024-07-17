from discord_webhook import DiscordWebhook

webhook_url = ""


def discord_send(mes: str, url: str):
    webhook = DiscordWebhook(url=url, content=mes)
    webhook.execute()

if __name__ == "__main__":
    discord_send("Hello, World!", url = webhook_url)
