import discord
from os import getenv
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

# cobalt says: why make a separate bot instance?
bot = commands.Bot("test", intents=discord.Intents().all(),)


@bot.event
async def on_ready():
    # again - use the sparkplug instance
    await bot.http.bulk_upsert_global_commands(bot.application_id, [])
    print("commands reset")

# token is stored in SparkPlug.TOKEN variable defined in __init__
bot.run(getenv("TOKEN"))

# honestly, what's the use of this file? you could include this in an owner-only cog using the proper instance