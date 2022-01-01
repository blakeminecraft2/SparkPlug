from logging import NullHandler
import discord
from time import time
import platform
from typing import IO, Union, Optional

from discord.ext.commands.help import Paginator
from lib.views import Invite
from datetime import datetime
import textwrap
import contextlib
from discord.ext import commands 
import io

def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:][:-3])

class Utils(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="ping", brief="Ping the bot", description="Get the bot's latency values (websocket and REST)")
    async def ping(self, ctx):

        api_start = time()
        msg = await ctx.send("Ping...")
        api_end = time()
        
        em = discord.Embed(title="Pong!", color=ctx.author.color, timestamp=datetime.utcnow())
        em.set_author(url="https://cdn.discordapp.com/attachments/922830600849752104/922830618964942868/lightbulb-variant-outline.png", name="")
        em.add_field(name="WS Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        em.add_field(name="REST Latency", value=f"{round((api_end - api_start) * 1000)}ms", inline=True)
        await msg.edit(content=None, embed=em)


    @commands.command(name="about", aliases=["version", "info"], brief="Get version info about the bot")
    async def about(self, ctx):
        em = discord.Embed(title="About", color=ctx.guild.me.color, timestamp=datetime.utcnow())
        em.add_field(name="Bot version", value=self.bot.__version__, inline=True)
        em.add_field(name="Python version", value=platform.python_version(), inline=True)
        em.add_field(name="Discord.py version", value=discord.__version__, inline=True)
        
        # sorting this out soon
        await ctx.send(embed=em, view=Invite(ctx)) 

    @commands.command(name="userinfo", aliases=["whois", "uinfo", "user"], brief="Get information on a user")
    async def userinfo(self, ctx:commands.Context, member:discord.Member=None):
        if member is None:
            member = ctx.author
        em = discord.Embed(title="UserInfo", color=ctx.author.color,description=member.nick , timestamp=datetime.utcnow())
        em.set_thumbnail(url=member.avatar.url)
        if not member.banner is None:
            em.set_image(url=member.banner.url)
        em.add_field(name="username", value=member)
        em.add_field(name="ID", value=member.id)
        em.add_field(name="nitro since", value=member.premium_since)
        em.add_field(name="bot", value=member.bot)
        em.add_field(name="top role", value=member.top_role)
        await ctx.send(embed=em)

    @commands.command(name="serverinfo")
    async def serverinfo(self, ctx: commands.Context):
        em = discord.Embed(title="Server info", color=ctx.author.color)
        em.set_thumbnail(url=ctx.guild.icon.url)
        em.add_field(name="name", value=ctx.guild.name)
        em.add_field(name="nitro boosts", value=str(ctx.guild.premium_subscription_count))
        em.add_field(name="boost tier", value=str(ctx.guild.premium_tier))
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Utils(bot))