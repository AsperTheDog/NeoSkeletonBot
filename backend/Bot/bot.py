import asyncio
import os

from disnake import Intents
from disnake.ext.commands import Bot
from Bot.listener import EventListener
import yaml


client = Bot(intents=Intents.all())
client.add_cog(EventListener(client))


@client.event
async def on_ready():
    print(f'Logged on as {client.user}!')
    client.errCh = {}
    client.errMsg = {}


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    exec("from fsmLogic.mains import *")
    exec("from fsmLogic.actionCodes import *")
    actionPaths = os.listdir("fsmLogic/actionCodes/custom")
    for pth in actionPaths:
        if pth != ".gitkeep":
            exec("from fsmLogic.actionCodes.custom." + pth + " import *")


with open('Bot/bot.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)


def runBot():
    print("starting client")
    client.run(data['token'])


if __name__ == "__main__":
    runBot()