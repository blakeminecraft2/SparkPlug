import discord
import aiohttp
from discord.ext import commands

class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji = "<:image:927276284999008276>"

    @commands.command()
    async def cat(self, ctx: commands.Context) -> discord.Message:
        async with aiohttp.ClientSession() as session:
            image = await session.get('https://some-random-api.ml/animal/cat')
            image = await image.json()

        embed = discord.Embed(title="Cat", color=ctx.author.color)
        embed.set_image(url=image['image'])
        await ctx.send(embed=embed)

    @commands.command()
    async def dog(self, ctx: commands.Context) -> discord.Message:
        async with aiohttp.ClientSession() as session:
            image = await session.get('https://some-random-api.ml/animal/dog')
            image = await image.json()

        embed = discord.Embed(title="Dog", color=ctx.author.color)
        embed.set_image(url=image['image'])
        await ctx.send(embed=embed)


    @commands.command()
    async def maid(self, ctx: commands.Context) -> discord.Message:
        async with aiohttp.ClientSession() as session:
            img = await session.get('https://api.waifu.im/sfw/maid/')
            image = await img.json()

        embed = discord.Embed(title="Maid", color=ctx.author.color)
        embed.set_image(url=image['images'][0]['url'])
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Image(bot))