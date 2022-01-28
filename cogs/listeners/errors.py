import discord
from discord.ext import commands

class errors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self,ctx: commands.Context,error):
        if isinstance(error, commands.MissingPermissions):
            em = discord.Embed(title="<:alert:934067010969698336> Oh fiddlesticks", description="You do not have the permission to do this")
            await ctx.send(embed=em)
        else:
            em = discord.Embed(title="<:error:934067743358087199> Error", description=f"```{error}```")
            await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(errors(bot))
