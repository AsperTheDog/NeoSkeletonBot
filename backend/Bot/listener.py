from disnake.ext import commands

from fsmLogic.boardManager import BoardManager


class EventListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.index = 0

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        msgData = {
            'content': message.content,
            'channel': message.channel.id
        }
        BoardManager.sendGlobalEvent(self.bot, "on message received", msgData, str(message.guild.id))

