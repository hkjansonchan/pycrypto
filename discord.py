from discord_webhook import DiscordWebhook

webhook_url = ""


def dcsend(mes: str):
    webhook = DiscordWebhook(url=webhook_url, content=mes)
    webhook.execute()

if __name__ == "__main__":
    dcsend("Hello, World!")
