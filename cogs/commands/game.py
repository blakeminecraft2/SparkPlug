import discord
from discord.ext import commands
from lib.views import RPS

class Games(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.emoji = "<:gamepad:927592545100369950>"

    #we should make a tic tac toe command here
    @commands.command(slash_command=False)
    async def gametest(self,ctx):
        await ctx.send("Test done")

    @commands.command()
    async def rps(self,ctx):
        msg = await ctx.send("RPS!")
        await msg.edit("RPS!", view=RPS(ctx, msg))

def setup(bot):
    bot.add_cog(Games(bot))