import discord
from discord.ext import commands

class errors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Oh fiddlesticks, you do not have the permission to do this")
        else:
            await ctx.send(error)


def setup(bot):
    bot.add_cog(errors(bot))
