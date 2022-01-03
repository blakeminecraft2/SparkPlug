import discord
from discord.ext import commands

class gjoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self,guild: discord.Guild):
        em = discord.Embed(title="SparkPlug",description="<:sparkplug:922842179045589032> bot is currently online!" , color=discord.Color.greyple())
        await guild.system_channel.send(embed=em)

def setup(bot):
    bot.add_cog(gjoin(bot))