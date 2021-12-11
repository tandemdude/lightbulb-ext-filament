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

__all__ = ["pass_options"]

from lightbulb import context


def pass_options(func):
    """
    First order decorator that causes the decorated command callback function
    to have all options provided by the context passed as **keyword** arguments
    on invocation. This allows you to access the options directly instead of through the
    context object.

    This decorator **must** be below all other command decorators.

    Example:

        .. code-block:: python

            @lightbulb.option("text", "Text to repeat")
            @filament.utils.prefix_command("echo", "Repeats the given text")
            @filament.utils.pass_options
            async def echo(ctx, text):
                await ctx.respond(text)
    """

    async def decorated(ctx: context.Context) -> None:
        await func(ctx, **ctx.raw_options)

    return decorated
