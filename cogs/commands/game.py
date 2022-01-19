import discord
from discord.ext import commands

class Games(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.emoji = "<:gamepad:927592545100369950>"

    #we should make a tic tac toe command here
    @commands.command(slash_command=False)
    async def gametest(self,ctx):
        await ctx.send("Test done")

def setup(bot):
    bot.add_cog(Games(bot))