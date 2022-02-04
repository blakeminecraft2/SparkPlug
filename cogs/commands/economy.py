import discord
import aiohttp
import random
import json
import aiosqlite
from discord.ext import commands

class functions():

    async def get_info(member: discord.Member) -> tuple[int, int]:
            async with aiosqlite.connect("db/main.db") as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT * FROM economy WHERE user_id = ?", (member.id,))
                    result = await cur.fetchone()
                    return result

    async def update_wallet(member: discord.Member, wallet: int):
            async with aiosqlite.connect("db/main.db") as conn:
                async with conn.cursor() as cur:
                    await cur.execute("UPDATE economy SET wallet = ? WHERE user_id = ?", (wallet, member.id))
                    await conn.commit()

    async def update_bank(member: discord.Member, bank: int):
            async with aiosqlite.connect("db/main.db") as conn:
                async with conn.cursor() as cur:
                    await cur.execute("UPDATE economy SET bank = ? WHERE user_id = ?", (bank, member.id))
                    await conn.commit()



    async def open_account(member: discord.Member):
            async with aiosqlite.connect("db/main.db") as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT * FROM economy WHERE user_id = ?", (member.id,))
                    result = await cur.fetchone()
                    if result:
                        return
                    else:
                        await cur.execute("INSERT INTO economy(wallet, bank, user_id) VALUES (?,?,?)", (200,200,member.id))
                        await conn.commit()

class Economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.emoji = "<:cash:927276284780892161>"

    @commands.group(name="bank", brief="Bank management", invoke_without_command=True)
    async def bank(self, ctx):
        await functions.open_account(ctx.author)
        await ctx.send("commands: balance, deposit, withdraw")

    @bank.command(name="balance", aliases=["bal"], brief="check your balance")
    async def balance(self,ctx,member:discord.Member = None):
        if member is None:
            member = ctx.author
        await functions.open_account(member)

        data = await functions.get_info(member)

        em = discord.Embed(title="balance", color=ctx.author.color)
        em.add_field(name="wallet <:proton:923587178796302406>", value=data[0])
        em.add_field(name="bank :pound:", value=data[1])
        await ctx.send(embed=em)

    @bank.command(name="deposit", aliases=["dep"])
    async def deposit(self,ctx, amount: int):
        await functions.open_account(ctx.author)

        data = await functions.get_info(ctx.author)

        if int(data[0]) < amount:
            return
        
        await functions.update_wallet(ctx.author, data[0] - amount)
        await functions.update_bank(ctx.author, data[1] + amount)
        await ctx.send("done")

    @bank.command(name="withdraw", aliases=["with"])
    async def withdraw(self,ctx, amount: int):
        await functions.open_account(ctx.author)

        data = await functions.get_info(ctx.author)

        if int(data[1]) < amount:
            return
        
        await functions.update_wallet(ctx.author, data[0] + amount)
        await functions.update_bank(ctx.author, data[1] - amount)
        await ctx.send("done")

    @commands.command(name="steal")
    async def steal(self, ctx: commands.Context, user: discord.Member, amount: int):
        await functions.open_account(ctx.author)

        data = await functions.get_info(user)
        userdata = await functions.get_info(ctx.author)

        if data[0] <= amount:
            await ctx.send("user is too poor :sad:")
            return

        await functions.update_wallet(ctx.author, userdata[0] + amount)

        await functions.update_wallet(user, data[0] - amount)

        await ctx.send("stolen!")

    

#this not working for some reason

def setup(bot):
    bot.add_cog(Economy(bot))