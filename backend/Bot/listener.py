import asyncio
from disnake.ext import commands


class EventListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.index = 0
        self.queue = asyncio.Queue()

    @commands.Cog.listener()
    async def on_message(self, message):
        print("message got from", message.author.name)