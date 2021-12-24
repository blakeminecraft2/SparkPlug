import discord
from discord.ext import commands
from discord.ui import View, Button

class Invite(View):
    def __init__(self, ctx):
        self.ctx = ctx
        self.user = self.ctx.author
        super().__init__()

        self.invite_button = Button(label="Invite me", style=discord.ButtonStyle.blurple, emoji="✉️", url="http://sparkpluginv.itzfinleyplayz.org/")
        self.add_item(self.invite_button)

        self.website = Button(label="Website", style=discord.ButtonStyle.blurple, emoji="🌐", url="https://www.botrepublic.itzfinleyplayz.org/smartplug")
        self.add_item(self.website)
    