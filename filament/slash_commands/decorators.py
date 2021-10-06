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
import typing

import hikari
from lightbulb.slash_commands.commands import OPTION_TYPE_MAPPING
from lightbulb.slash_commands.commands import _get_choice_objects_from_choices

from filament.slash_commands import commands

__all__ = ["slash_command", "with_option", "with_checks"]


def slash_command(*, description: str, name: str = None, guilds: typing.Optional[typing.Iterable[int]] = None):
    """
    Decorator that turns an async function into a slash command object.

    Keyword Args:
        description: The description of the slash command.
        name: The name of the slash command. Defaults to the decorated function's name in lowercase.
        guilds: The guilds that the command should be created in. Defaults to ``None`` (global command).

    Example:

        .. code-block:: python

            @filament.slash_command(description="Checks that the bot is alive")
            async def ping(context):
                await context.respond("Pong!")
    """

    def decorate(func) -> commands._SlashCommand:
        nonlocal name, guilds

        name = (name or func.__name__).lower()
        guilds = guilds if guilds is not None else []

        return commands._SlashCommand(name, description, guilds, func)

    return decorate


def with_option(
    *,
    type: typing.Type,
    name: str,
    description: str,
    default: typing.Any = None,
    choices: typing.Sequence[typing.Any] = None,
):
    """
    Decorator that adds an option to a slash command.

    Keyword Args:
        type: The type of the option.
        name: The name of the option.
        description: The description of the option.
        default: The default value for the option. Defaults to ``None``.
        choices: The choices for the option. Defaults to ``None`` (no choices).

    Example:

        .. code-block:: python

            @filament.with_option(type=str, name="text", description="text to repeat")
            @filament.slash_command(description="Repeats the input from the user")
            async def echo(context):
                await context.respond(context.options.text)
    """

    def decorate(cmd: commands._SlashCommand) -> commands._SlashCommand:
        nonlocal type, choices

        required = typing.get_origin(type) is typing.Union and None.__class__ in type
        type = OPTION_TYPE_MAPPING[typing.get_args(type)[0] if typing.get_origin(type) is typing.Union else type]
        choices = _get_choice_objects_from_choices(choices) if choices is not None else []

        cmd.add_option(
            hikari.CommandOption(
                name=name,
                description=description,
                type=type,
                is_required=required,
                **({"choices": choices} if choices else {}),
            ),
            default,
        )

        return cmd

    return decorate


def with_checks(check1, *checks):
    """
    Decorator that adds checks to a slash command.

    Args:
        check1: First check to add to the slash command.
        *checks: Additional checks to add to the slash command.

    Example:

        .. code-block:: python

            @filament.with_checks(lightbulb.owner_only)
            @filament.slash_command(name="ping", description="Repeats the input from the user")
            async def owner_only_ping(context):
                await context.respond("Pong!")
    """

    def decorate(cmd: commands._SlashCommand) -> commands._SlashCommand:
        for check in [check1, *checks]:
            cmd.add_check(check)
        return cmd

    return decorate