import asyncio

from disnake.ext.commands import Bot
from Bot.listener import EventListener
import yaml


class MyClient(Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')


with open('Bot/bot.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

client = MyClient()
client.add_cog(EventListener(client))


def runBot():
    print("starting client")
    client.run(data['token'])
