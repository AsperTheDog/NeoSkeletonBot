from disnake.ext import commands


class InteractiveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot