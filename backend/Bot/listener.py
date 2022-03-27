import disnake
from disnake.ext import commands
import traceback

from fsmLogic.boardManager import BoardManager
from Bot import utils


class EventListener(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.index = 0

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author == self.bot.user:
            return
        BoardManager.sendGlobalEvent(self.bot, "on message received", utils.formatMessage(message, [message.id]), str(message.guild.id))

    # TODO: resto de listenes + scheduled
