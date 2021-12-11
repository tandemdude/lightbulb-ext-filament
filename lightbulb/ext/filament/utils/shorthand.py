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
from __future__ import annotations

__all__ = ["prefix_command", "slash_command", "prefix_slash_command"]

import typing as t

from lightbulb import commands
from lightbulb import decorators


def prefix_command(name: str, description: str, **kwargs: t.Any):
    """
    Shorthand decorator allowing you to easily define a prefix command. This decorator
    takes the same arguments as :obj:`lightbulb.decorators.command`.

    Example:

        .. code-block:: python

            @filament.utils.prefix_command("foo", "test command")
            async def foo(ctx):
                ...
    """

    def decorate(func) -> commands.CommandLike:
        func = decorators.implements(commands.PrefixCommand)(func)
        return decorators.command(name, description, **kwargs)(func)

    return decorate


def slash_command(name: str, description: str, **kwargs: t.Any):
    """
    Shorthand decorator allowing you to easily define a slash command. This decorator
    takes the same arguments as :obj:`lightbulb.decorators.command`.

    Example:

        .. code-block:: python

            @filament.utils.slash_command("foo", "test command")
            async def foo(ctx):
                ...
    """

    def decorate(func) -> commands.CommandLike:
        func = decorators.implements(commands.SlashCommand)(func)
        return decorators.command(name, description, **kwargs)(func)

    return decorate


def prefix_slash_command(name: str, description: str, **kwargs: t.Any):
    """
    Shorthand decorator allowing you to easily define a prefix and slash command. This decorator
    takes the same arguments as :obj:`lightbulb.decorators.command`.

    Example:

        .. code-block:: python

            @filament.utils.prefix_slash_command("foo", "test command")
            async def foo(ctx):
                ...
    """

    def decorate(func) -> commands.CommandLike:
        func = decorators.implements(commands.SlashCommand, commands.PrefixCommand)(func)
        return decorators.command(name, description, **kwargs)(func)

    return decorate
