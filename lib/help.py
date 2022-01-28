from typing import Optional, Set
import discord
from discord.ext import commands
from discord.ext.commands.core import Group
from discord.ui.item import V
from discord.ui import button
from dotenv.main import load_dotenv

class HelpDrop(discord.ui.Select):
    def __init__(self,help_command: "SparkHelp", options: list[discord.SelectOption]):
        super().__init__(placeholder="Choose a category...", min_values=1, max_values=1, options=options)
        self._help_command = help_command

    async def callback(self, interaction: discord.Interaction):
        em = (
            await self._help_command._cog_help_embed(self._help_command.context.bot.get_cog(self.values[0]))
            if self.values[0] != self.options[0].value
            else await self._help_command._home_help_embed(self._help_command.get_bot_mapping())
            )
        await interaction.response.edit_message(embed=em)


class HelpView(discord.ui.View):
    def __init__(self, ctx: commands.Context, help_command, options: list[discord.SelectOption] , *, timeout: Optional[float] = 120.0):
        super().__init__(timeout=timeout)
        self.options = options
        self.add_item(HelpDrop(help_command, options))
        self._help_command = help_command
        self.ctx = ctx

    @button(label="", emoji="🗑️", style=discord.ButtonStyle.red)
    async def callback(self, button, interaction: discord.Interaction):
        await self.ctx.message.add_reaction("🗑️")
        await interaction.message.delete()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("A user has fallen into the wrong view in discord city. Hey!", ephemeral=True)
            return False
        else:
            return True    


class SparkHelp(commands.MinimalHelpCommand):

    async def _cog_select_options(self) -> list[discord.SelectOption]:
        options: list[discord.SelectOption] = []
        options.append(discord.SelectOption(
            label="Home",
            emoji="<:home:934064768619257857>",
            description="Go back to the main menu"
        ))

        for cog, command_set in self.get_bot_mapping().items():
            filtered = await self.filter_commands(command_set, sort=True)
            if not filtered:
                continue
            options.append(discord.SelectOption(
                label=cog.qualified_name if cog else "No category",
                emoji=cog.emoji if cog else "<:sparkplug:922842179045589032>",
                description=cog.description[:100] if cog and cog.description else None
            )
            )
        return options

    
    async def _help_command(self, title: str, description: str = None, mapping: Optional[str] = None, command_set: Optional[Set[commands.Command]] = None):
        em = discord.Embed(title=title, description=description, color=discord.Color.lighter_grey())
        em.set_author(icon_url=self.context.bot.user.avatar, name="SparkPlug")
        if command_set:
            filtered = await self.filter_commands(command_set, sort=True)
            for command in filtered:
                em.add_field(name=f"`{self.get_command_signature(command)}`", value=command.help, inline=True)
        elif mapping:
            for cog, command_set in mapping.items():
                filtered = await self.filter_commands(command_set, sort=True)
                if not filtered:
                    continue
                name = f"{cog.emoji if cog else '<:sparkplug:922842179045589032>'}{cog.qualified_name if cog else 'No Category'}" 
                cmd_list = "\u2002".join(
                    f"`{cmd.name}`" for cmd in filtered
                )
                value = (
                    f"{cog.description}\n{cmd_list}"
                    if cog and cog.description
                    else cmd_list
                )
                em.add_field(name=name, value=value, inline=True)
        
        return em

    async def _home_help_embed(self, mapping) -> discord.Embed:
        return await self._help_command(
            title="Help",
            description=self.context.bot.description,
            mapping=mapping)

    async def send_bot_help(self, mapping):
        options = await self._cog_select_options()
        await self.context.send(embed=await self._home_help_embed(mapping), view=HelpView(ctx = self.context,help_command=self, options=options, timeout=20))

    async def send_command_help(self, command: commands.Command):
        em = await self._help_command(
            title=command.qualified_name,
            description=self.get_command_signature(command),
        )
        await self.context.send(embed=em)
    
    async def send_group_help(self, group: commands.Group):
        em = await self._help_command(
            title=group.qualified_name,
            description=group.help,
            command_set=group.commands if isinstance(group, commands.Group) else None,
        )
        await self.context.send(embed=em)

    async def _cog_help_embed(self, cog: commands.Cog) -> discord.Embed:
        return await self._help_command(
                title=f"<:applicationcog:936567883813761024> **Cog** {cog.qualified_name}",
                description=cog.description,
                command_set=cog.get_commands()
                )

    async def send_cog_help(self, cog: commands.Cog):
        
        await self.context.send(embed=await self._cog_help_embed(cog))