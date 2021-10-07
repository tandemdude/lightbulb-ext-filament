# -*- coding: utf-8 -*-
# Copyright © tandemdude 2020-present
#
# This file is part of Filament.
#
# Filament is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Filament is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Filament. If not, see <https://www.gnu.org/licenses/>.
"""
Filament provides an alternative, decorator-based implementation of slash commands as opposed
to the class-based system provided by hikari-lightbulb.

This implementation is more similar to the prefix/message commands implementation present in
hikari-lightbulb so may feel more familiar to you.

Creating a Simple Slash Command
===============================

Creating a simple slash command is very easy, and can be done in very few lines of code:

.. code-block:: python

    import filament
    import lightbulb

    bot = lightbulb.Bot(...)

    @filament.with_option(type=str, name="text", description="text to repeat")
    @filament.slash_command(description="Repeats the input")
    async def echo(context: lightbulb.SlashCommandContext) -> None:
        await context.respond(context.options.text)

    bot.add_slash_command(echo)
    bot.run()

"""
import typing

import lightbulb

from filament.slash_commands import commands
from filament.slash_commands import decorators
from filament.slash_commands.commands import *
from filament.slash_commands.decorators import *

__all__ = [
    *decorators.__all__,
    *commands.__all__,
    "autodiscover_slash_commands",
    "autoremove_slash_commands",
]


def _get_slash_commands_in_current_extension(
    bot: lightbulb.Bot,
) -> typing.List[
    typing.Union[
        lightbulb.SlashCommand, lightbulb.SlashCommandGroup, commands._SlashCommand, commands._SlashCommandGroup
    ]
]:
    cmds = []
    cmds.extend(bot._get_slash_commands_in_current_extension())

    for item in dir(bot._current_extension):
        obj = getattr(bot._current_extension, item)
        if isinstance(obj, (commands._SlashCommand, commands._SlashCommandGroup)):
            cmds.append(obj)
    return cmds


def autodiscover_slash_commands(bot: lightbulb.Bot, create: bool = False) -> None:
    """
    Automatically discovers all lightbulb slash command classes, and filament slash command
    objects in the current extension and adds each of them to the bot.

    This should **only** be used in an extension's ``load`` function.

    Args:
        bot (:obj:`lightbulb.command_handler.Bot`): The bot instance to add the commands to.
        create (:obj:`bool`): Whether or not to send a create request to discord when the command is added.
            Defaults to ``False``.

    Returns:
        ``None``
    """
    if bot._current_extension is None:
        return

    for cmd in _get_slash_commands_in_current_extension(bot):
        bot.add_slash_command(cmd, create=create)


def autoremove_slash_commands(bot: lightbulb.Bot, delete: bool = False) -> None:
    """
    Automatically discovers all lightbulb slash command classes, and filament slash command
    objects in the current extension and removes each of them from the bot.

    This should **only** be used in an extension's ``unload`` function.

    Args:
        bot (:obj:`lightbulb.command_handler.Bot`): The bot instance to remove the commands from.
        delete (:obj:`bool`): Whether or not to delete the command from discord when it is removed.
            Defaults to ``False``.

    Returns:
        ``None``
    """
    if bot._current_extension is None:
        return

    for cmd in _get_slash_commands_in_current_extension(bot):
        cmd = cmd if isinstance(cmd, (commands._SlashCommand, commands._SlashCommandGroup)) else cmd(bot)
        bot.remove_slash_command(cmd.name, delete=delete)
