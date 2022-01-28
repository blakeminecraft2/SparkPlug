import discord
from random import randrange
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.emoji = "<:castle:936549910747176990>"

    @commands.command()
    async def cool(self,ctx,member: discord.Member = None):
        if member == None:
            member = ctx.author
        
        em = discord.Embed(title="Coolness meter :thermometer:", color=member.color, description=f"{member.display_name} is {randrange(0,100)}% cool!")
        await ctx.send(embed=em)

    @commands.command()
    async def ratio(self,ctx: commands.Context):
        msg = await ctx.send("Ratio!")
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")


def setup(bot):
    bot.add_cog(Fun(bot))