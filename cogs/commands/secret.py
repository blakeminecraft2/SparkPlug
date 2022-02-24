import discord
from discord.ext import commands

class Secret(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji = "🐻‍❄️"

    @commands.command(slash_command=False)
    async def Secret(self,ctx: commands.Context,user: discord.Member):
        msg = await ctx.send(f"You walk up to *{user.name}* and fuck them in the ass so hard it comes out their nose and mouth")
        await msg.add_reaction("😻")

def setup(bot):
    bot.add_cog(Secret(bot))
