from datetime import time, timedelta
import discord
import aiosqlite
from typing import Optional, Union
from discord.ext import commands
from discord.utils import utcnow

async def open(member: discord.Member):
            async with aiosqlite.connect("db/main.db") as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT * FROM warns WHERE user_id = ? AND guild_id = ?", (member.id,member.guild.id))
                    result = await cur.fetchone()
                    if result:
                        return
                    else:
                        await cur.execute("INSERT INTO warns(guild_id, user_id, warns) VALUES (?,?,?)", (member.guild.id, member.id, 0))
                        await conn.commit()

async def getdata(member: discord.Member):
            async with aiosqlite.connect("db/main.db") as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT * FROM warns WHERE user_id = ? AND guild_id = ?", (member.id,member.guild.id))
                    result = await cur.fetchone()
                    return result

async def update(member: discord.Member, amt: int):
            async with aiosqlite.connect("db/main.db") as conn:
                async with conn.cursor() as cur:
                    await cur.execute("UPDATE warns SET warns = ? WHERE user_id = ? AND guild_id = ?", (amt, member.id, member.guild.id))
                    await conn.commit()


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.emoji = "<:gavel:927276284592144425>"
    
    @commands.command(name="slowmode")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self,ctx,length: int = commands.Option(description="the length of the slowmode in seconds")):
        await ctx.channel.edit(slowmode_delay=length)
        await ctx.send(f":snail: OK, set slowmode to {length} seconds!")

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, members: commands.Greedy[discord.Member], *, reason: Optional[str] = commands.Option(description="Why are you kicking these members?", default="No reason provided")):
       for member in members:
            try:
                await member.send(f"You have been kicked from {ctx.guild}\nReason: {reason}")
            except discord.errors.Forbidden:
                await ctx.send(f"I could not DM {member}")
            await member.kick(reason=reason)
            await ctx.send(f":boot: Kicked user {member}")

    @commands.command(name="ban", brief="Ban users by ID or tag", description="Ban members from the server - also supports ID arguments for 'hackbanning'")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, members: commands.Greedy[Union[discord.Member,discord.User]], delete_message_days: Optional[int] = commands.Option(description="How many days of messages from the members should be deleted?", default=0), *, reason: Optional[str] = commands.Option(description="Why are you banning these members?", default="No reason provided")):
       for member in members:
            if isinstance(member,discord.Member):
                try:
                    await member.send(f"You have been banned from {ctx.guild}\nReason: {reason}")
                except discord.errors.Forbidden:
                    await ctx.send(f"I could not DM {member}")
                await member.ban(reason=reason, delete_message_days=delete_message_days)
            else:
                member = await self.bot.fetch_user(int(member))
                await ctx.guild.ban(member,reason=reason)
            await ctx.send(f":hammer: Banned user {member}")

    @commands.command(name="mute",brief="mute (timeout) a member")
    @commands.has_permissions(moderate_members=True)
    async def mute(self,ctx,member:discord.Member, seconds:int=60):
        amt = utcnow() + timedelta(seconds=seconds)
        await member.edit(timeout_until=amt)
        em = discord.Embed(title="Timeout")
        em.add_field(name="user effected", value=member.mention, inline=False)
        em.add_field(name="length", value=seconds)
        em.add_field(name="executed by", value=ctx.author.mention, inline=False)
        await ctx.send(embed=em)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def purge(self,ctx:commands.Context,amt: int):
        await ctx.channel.purge(limit=amt)

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def warnings(self, ctx, member: discord.Member):
        await open(member)
        data = await getdata(member)
        await ctx.send(f"user has {data[2]} warnings")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def warn(self, ctx, member: discord.Member):
        await open(member)
        data = await getdata(member)

        await update(member, data[2]+1)

        await ctx.send(f"warned user")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def revoke(self, ctx, member: discord.Member, amt: int):
        await open(member)
        data = await getdata(member)

        await update(member, data[2]-amt)

        await ctx.send(f"revoked warnings")
            
def setup(bot):
    bot.add_cog(Moderation(bot))