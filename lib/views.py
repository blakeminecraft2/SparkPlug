import discord
from discord.ext import commands
from discord.ui import View, Button, button
from random import choice

class Invite(View):
    def __init__(self, ctx):
        self.ctx = ctx
        self.user = self.ctx.author
        super().__init__()

        self.invite_button = Button(label="Invite me", style=discord.ButtonStyle.blurple, emoji="✉️", url="http://sparkpluginv.itzfinleyplayz.org/")
        self.add_item(self.invite_button)

        self.website = Button(label="Website", style=discord.ButtonStyle.blurple, emoji="🌐", url="https://www.botrepublic.itzfinleyplayz.org/smartplug")
        self.add_item(self.website)

class RPS(View):
    def __init__(self, ctx: commands.Context, msg: discord.Message):
        self.ctx = ctx
        self.message = msg
        self.user = self.ctx.author
        super().__init__()
    async def process(self, rps_user: str):
        rps_cpu = choice(["rock", "paper", "scissors"])
        checks = {
            ("rock", "scissors"): "win",
            ("scissors", "rock"): "loss",
            ("paper", "scissors"): "loss",
            ("paper", "rock"): "win",
            ("rock", "paper"): "loss",
            ("scissors", "paper"): "win",
        }
        result = checks[(rps_user, rps_cpu)] if rps_user != rps_cpu else "draw"

        if result == "win":
            await self.ctx.send(f"You win, I chose {rps_cpu}")
        if result == "loss":
            await self.ctx.send(f"You lose, I chose {rps_cpu}")
        if result == "draw":
            await self.ctx.send(f"Draw, I chose {rps_cpu}")
        await self.message.edit("RPS -- Finished", view=None)
        await self.message.add_reaction("✅")
        self.stop()
    
    @button(label="Rock")
    async def rock(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.user:
            return
        return await self.process("rock")

    @button(label="Paper")
    async def paper(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.user:
            return
        return await self.process("paper")
    
    @button(label="Scissors")
    async def scissors(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.user:
            return
        return await self.process("scissors")