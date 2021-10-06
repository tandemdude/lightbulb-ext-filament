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
        else:
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
