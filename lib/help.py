from typing import Optional, Set
import discord
from discord.ext import commands
from discord.ext.commands.core import Group

class SparkHelp(commands.MinimalHelpCommand):
    
    async def _help_command(self, title: str, description: str = None, mapping: Optional[str] = None, command_set: Optional[Set[commands.Command]] = None):
        em = discord.Embed(title=title, description=description, color=discord.Color.lighter_grey())
        if command_set:
            filtered = await self.filter_commands(command_set, sort=True)
            for command in filtered:
                em.add_field(name=f"`self.get_command_signature(command)`", value=command.help, inline=False)
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
                em.add_field(name=name, value=value, inline=False)
        
        return em
    
    async def send_bot_help(self, mapping):
        em = await self._help_command(
            title="SparkPlug",
            description=self.context.bot.description,
            mapping=mapping
        )
        await self.get_destination().send(embed=em)

    async def send_command_help(self, command: commands.Command):
        em = await self._help_command(
            title=command.qualified_name,
            description=command.help
        )
        await self.get_destination().send(embed=em)
    
    async def send_group_help(self, group: commands.Group):
        em = await self._help_command(
            title=group.qualified_name,
            description=group.help,
            command_set=group.commands if isinstance(group, commands.Group) else None,
        )
        await self.get_destination().send(embed=em)