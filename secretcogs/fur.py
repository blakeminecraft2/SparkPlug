import discord
from discord.ext import commands

class Furry(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji = "🐻‍❄️"

    @commands.command(slash_command=False)
    async def pet(self,ctx: commands.Context,user: discord.Member):
        msg = await ctx.send(f"You walk up to *{user.name}* and pat them on the head.")
        await msg.add_reaction("😻")

    @commands.command(slash_command=False)
    async def hug(self,ctx: commands.Context,user: discord.Member):
        msg = await ctx.send(f"You walk up to *{user.name}* and squish them with your arms!")
        await msg.add_reaction("😻")

    @commands.command(slash_command=False)
    async def boop(self,ctx: commands.Context,user: discord.Member):
        msg = await ctx.send(f"You walk up to *{user.name}* and boop their nose. 🙊")
        await msg.add_reaction("😻")

    @commands.command(slash_command=False)
    async def bark(self,ctx: commands.Context,user: discord.Member):
        msg = await ctx.send(f"You bark at *{user.name}*.")
        await msg.add_reaction("🐶")

    @commands.command(slash_command=False)
    async def bite(self,ctx: commands.Context,user: discord.Member):
        msg = await ctx.send(f"You give *{user.name}* a little munch.")
        await msg.add_reaction("😺")

def setup(bot):
    bot.add_cog(Furry(bot))