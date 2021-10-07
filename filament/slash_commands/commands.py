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
import lightbulb

__all__ = ["slash_command_group"]


class _SlashSubCommand(lightbulb.SlashSubCommand):
    def __init__(self, name: str, description: str, callback) -> None:
        self.bot = None
        super().__init__(self.bot)
        self._name = name
        self._description = description
        self._callback = callback
        self._options = []
        self._checks = []
        self._defaults = {}

    def __call__(self, *args, **kwargs):
        if isinstance(args[0], lightbulb.Bot):
            self.bot = args[0]
            return self
        return super().__call__(*args, **kwargs)

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def checks(self) -> typing.Sequence[lightbulb.Check]:
        return self._checks

    def add_check(self, check):
        if not isinstance(check, lightbulb.Check):
            check = lightbulb.Check(check)
        self._checks.append(check)

    def add_option(self, option: hikari.CommandOption, default: typing.Any = None):
        self._options.append(option)
        self._defaults[option.name] = default

    def as_option(self) -> hikari.CommandOption:
        return hikari.CommandOption(
            name=self.name,
            description=self.description,
            type=hikari.OptionType.SUB_COMMAND,
            options=list(sorted(self._options, key=lambda o: o.is_required, reverse=True)),
            is_required=False,
        )

    async def callback(self, context: lightbulb.SlashCommandContext) -> None:
        return await self._callback(context)


class _SlashSubGroup(lightbulb.SlashSubGroup):
    def __init__(self, name: str, description: str) -> None:
        self.bot = None
        super().__init__(self.bot)
        self._name = name
        self._description = description
        self._subcommands = {}

    def __call__(self, *args, **kwargs):
        if isinstance(args[0], lightbulb.Bot):
            self.bot = args[0]
            for cmd in self._subcommands.values():
                cmd(self.bot)
            return self
        return super().__call__(*args, **kwargs)

    @property
    def name(self) -> str:
        return self.name

    @property
    def description(self) -> str:
        return self.description

    def subcommand(self, *, description: str, name: str = None) -> typing.Callable[..., _SlashSubCommand]:
        """
        Decorator to add a function to this sub-group as a subcommand.

        Keyword Args:
            description: The description of the subcommand
            name: The name of the subcommand, defaults to the function's name if not specified.

        Example:

            .. code-block:: python

                group = filament.slash_command_group(...)
                subgroup = group.subgroup(...)

                @subgroup.subcommand(description="Test subcommand")
                async def foo(context):
                    await context.respond("bar")
        """

        def decorate(func):
            cmd = _SlashSubCommand(name or func.__name__, description, func)
            self._subcommands[cmd.name] = cmd
            return cmd

        return decorate


class _SlashCommandGroup(lightbulb.SlashCommandGroup):
    def __init__(self, name: str, description: str, enabled_guilds: hikari.SnowflakeishSequence) -> None:
        self.bot = None
        super().__init__(self.bot)
        self._name = name
        self._description = description
        self._enabled_guilds = enabled_guilds
        self._subcommands = {}

    def __call__(self, *args, **kwargs):
        if isinstance(args[0], lightbulb.Bot):
            self.bot = args[0]
            for cmd in self._subcommands.values():
                cmd(self.bot)
            return self
        return super().__call__(*args, **kwargs)

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def enabled_guilds(self) -> typing.Optional[typing.Union[hikari.Snowflakeish, hikari.SnowflakeishSequence]]:
        return self._enabled_guilds

    def subgroup(self, name: str, *, description: str) -> _SlashSubGroup:
        """
        Creates a slash command sub-group object that subcommands can be bound to.

        Args:
            name: The name of the sub-group.

        Keyword Args:
            description: The description of the sub-group.

        Returns:
            Created slash command sub-group object.

        Example:

            .. code-block:: python

                group = filament.slash_command_group(...)
                subgroup = group.subgroup("foo", description="bar")
        """
        cmd = _SlashSubGroup(name, description)
        self._subcommands[cmd.name] = cmd
        return cmd

    def subcommand(self, *, description: str, name: str = None) -> typing.Callable[..., _SlashSubCommand]:
        """
        Decorator to add a function to this group as a subcommand.

        Keyword Args:
            description: The description of the subcommand
            name: The name of the subcommand, defaults to the function's name if not specified.

        Example:

            .. code-block:: python

                group = filament.slash_command_group(...)

                @group.subcommand(description="Test subcommand")
                async def foo(context):
                    await context.respond("bar")
        """

        def decorate(func):
            cmd = _SlashSubCommand(name or func.__name__, description, func)
            self._subcommands[cmd.name] = cmd
            return cmd

        return decorate


class _SlashCommand(lightbulb.SlashCommand):
    def __init__(
        self,
        name: str,
        description: str,
        enabled_guilds: hikari.SnowflakeishSequence,
        callback,
    ):
        self.bot = None
        super().__init__(self.bot)
        self._name = name
        self._description = description
        self._enabled_guilds = enabled_guilds
        self._callback = callback
        self._options = []
        self._checks = []
        self._defaults = {}

    def __call__(self, *args, **kwargs):
        if isinstance(args[0], lightbulb.Bot):
            self.bot = args[0]
            return self
        return super().__call__(*args, **kwargs)

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def enabled_guilds(
        self,
    ) -> typing.Optional[typing.Union[hikari.Snowflakeish, hikari.SnowflakeishSequence]]:
        return self._enabled_guilds

    @property
    def checks(self) -> typing.Sequence[lightbulb.Check]:
        return self._checks

    def add_check(self, check):
        if not isinstance(check, lightbulb.Check):
            check = lightbulb.Check(check)
        self._checks.append(check)

    def add_option(self, option: hikari.CommandOption, default: typing.Any = None):
        self._options.append(option)
        self._defaults[option.name] = default

    def get_options(self) -> typing.Sequence[hikari.CommandOption]:
        return list(sorted(self._options, key=lambda o: o.is_required, reverse=True))

    async def callback(self, context: lightbulb.SlashCommandContext) -> None:
        return await self._callback(context)


def slash_command_group(
    name: str, *, description: str, guilds: typing.Optional[hikari.SnowflakeishSequence] = None
) -> _SlashCommandGroup:
    """
    Creates a slash command group object that subcommands and subgroups can be bound to.

    Args:
        name: The name of the slash command group.

    Keyword Args:
        description: The description of the slash command group.
        guilds: The guilds that the command should be created in. Defaults to ``None`` (global command).

    Returns:
        Created slash command group object.

    Example:

        .. code-block:: python

            group = filament.slash_command_group("foo", description="test group")
    """
    return _SlashCommandGroup(
        name,
        description,
        guilds if guilds is not None else [],
    )
