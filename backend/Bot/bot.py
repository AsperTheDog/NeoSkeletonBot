import json
import os

from disnake import Intents
from disnake.ext.commands import Bot

from Bot.cmds import InteractiveCog
from Bot.listener import EventListener
import yaml

from database.dbManager import SkeletonDB

client = Bot(intents=Intents.all(), command_prefix="sk!")
client.add_cog(EventListener(client))
client.add_cog(InteractiveCog(client))
client.errCh = {}
client.errMsg = {}
client.db = SkeletonDB()
client.debug = True
client.safe = False


@client.event
async def on_ready():
    print(f'Logged on as {client.user}!')
    with open("fsmLogic/dataFiles/tracking/botGuilds.json", "w") as file:
        json.dump([guild.id for guild in client.guilds], file)


with open('Bot/bot.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)


def runBot(standalone=False):
    print("starting client")
    if standalone:
        exec("from fsmLogic.mains import *")
        exec("from fsmLogic.actionCodes import *")
        actionPaths = os.listdir("fsmLogic/actionCodes/custom")
        for pth in actionPaths:
            if pth != ".gitkeep":
                exec("from fsmLogic.actionCodes.custom." + pth + " import *")
    client.run(data['token'])


if __name__ == "__main__":
    runBot()