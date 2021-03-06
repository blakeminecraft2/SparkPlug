from logging import fatal
import os
from os import getenv
from pathlib import Path
import aiosqlite
import aiohttp
from lib.help import SparkHelp
import discord
from discord.ext import commands
from dotenv import load_dotenv


class SparkPlug(commands.AutoShardedBot):
    def __init__(self):

        load_dotenv()

        self.__version__ = getenv("VERSION")
        self.TOKEN = getenv("TOKEN")

        if not self.TOKEN:
            raise EnvironmentError("Must provide a Discord bot token")

        self.DEFAULT_PREFIX = getenv("DEFAULT_PREFIX", "sp-")

        super().__init__(
            command_prefix=commands.when_mentioned_or(self.DEFAULT_PREFIX),
            slash_commands=True,
            case_insensitive=False,
            intents=discord.Intents().all(),
            help_command=SparkHelp(),
            allowed_mentions=discord.AllowedMentions(
                users=True, replied_user=True, roles=False, everyone=False
            ),
        )

    def load_extensions(self):
        for extension in Path(r"cogs").glob("**/*.py"):
            extension = str(extension).replace("\\", ".")[:-3]
            self.load_extension(extension)
            print(f"loaded extension {extension}")
            
    def run(self, token: str = None):
        self.httpsession = aiohttp.ClientSession()
        self.load_extensions()
        super().run(token)
        
    async def close(self):
        await self.httpsession.close()
        await super().close()

    async def on_ready(self):
        print(f"Bot is online - logged in as {self.user}")
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="sp-help || /help"))
        print("Presence changed.")
