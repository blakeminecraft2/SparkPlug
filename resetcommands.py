import discord
from os import getenv
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

bot = commands.Bot("test", intents=discord.Intents().all(),)


@bot.event
async def on_ready():
    await bot.http.bulk_upsert_global_commands(bot.application_id, [])
    print("commands reset")

bot.run(getenv("TOKEN"))