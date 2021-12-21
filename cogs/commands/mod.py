import discord
from typing import Optional, Union
from discord.ext import commands


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
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
                member.send(f"You have been kicked from {ctx.guild}\nReason: {reason}")
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
                    member.send(f"You have been banned from {ctx.guild}\nReason: {reason}")
                except discord.errors.Forbidden:
                    await ctx.send(f"I could not DM {member}")
                await member.ban(reason=reason, delete_message_days=delete_message_days)
            else:
                member = await self.bot.fetch_user(int(member))
                await ctx.guild.ban(member,reason=reason)
            await ctx.send(f":hammer: Banned user {member}")
            
def setup(bot):
    bot.add_cog(Moderation(bot))