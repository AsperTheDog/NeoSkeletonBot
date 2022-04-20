import disnake
from disnake.ext import commands


class InteractiveCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description="Small command to test if the bot is working")
    async def ping(self, inter):
        await inter.response.send_message("Pong!")

    @commands.slash_command(description="turns debug on and off. If debug is on, extra info will be displayed on the terminal")
    async def toggleDebug(self, inter):
        self.bot.debug = not self.bot.debug
        await inter.response.send_message("Debug mode is now " + ("on" if self.bot.debug else "off"))

    @commands.slash_command(description="turns all executions off instantly and disables them")
    async def alarm(self, inter):
        self.bot.safe = True
        await inter.response.send_message("Alarm mode is on, the bot will not execute anything")

    @commands.slash_command(description="returns the bot to normal behavior")
    async def safe(self, inter):
        self.bot.safe = False
        await inter.response.send_message("Alarm mode is off, the bot will execute scripts")
