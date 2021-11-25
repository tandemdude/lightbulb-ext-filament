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

__all__ = ["opt", "option", "CommandLike"]

import abc
import collections
import functools
import typing as t

import hikari
import lightbulb
from lightbulb import commands
from lightbulb import context


def opt(name: str, description: str, **kwargs: t.Any):
    kwargs.setdefault("required", kwargs.get("default", hikari.UNDEFINED) is hikari.UNDEFINED)
    if not kwargs["required"]:
        kwargs.setdefault("default", None)
    return commands.OptionLike(name, description, **kwargs)


option = opt
"""Alias for :obj:`~opt`."""


class CommandLike(abc.ABC):
    _subcommands: t.Dict[t.Type[CommandLike], t.List[t.Type[CommandLike]]] = collections.defaultdict(list)
    _error_handlers: t.Dict[t.Type[CommandLike], t.Callable[[context.Context], t.Coroutine[t.Any, t.Any, bool]]] = {}
    _help_getters: t.Dict[t.Type[CommandLike], t.Callable[[commands.Command, context.Context], str]] = {}
    _check_exempts: t.Dict[
        t.Type[CommandLike], t.Callable[[context.Context], t.Union[bool, t.Coroutine[t.Any, t.Any, bool]]]
    ] = {}

    def __new__(cls, *args: t.Any, **kwargs: t.Any) -> commands.CommandLike:
        new = super().__new__(cls, *args, **kwargs)
        return new._as_lightbulb_commandlike()

    def _find_options(self) -> t.MutableMapping[str, commands.OptionLike]:
        options = {}
        for item in dir(self):
            obj = getattr(self, item)
            if isinstance(obj, commands.OptionLike):
                options[obj.name] = obj
        return options

    def _as_lightbulb_commandlike(self) -> commands.CommandLike:
        @functools.wraps(self.callback)
        async def _callback(*args: t.Any, **kwargs: t.Any) -> None:
            await self.callback(*args, **kwargs)

        setattr(_callback, "__cmd_types__", self.implements)

        return commands.CommandLike(
            _callback,
            self.name,
            self.description,
            self._find_options(),
            self.checks,
            self._error_handlers.get(self.__class__),
            self.aliases,
            self.guilds if not isinstance(self.guilds, int) else [self.guilds],
            [s() for s in self._subcommands.get(self.__class__, [])],
            self.parser,
            self.cooldown_manager,
            self._help_getters.get(self.__class__),
            self.auto_defer,
            self.ephemeral,
            self._check_exempts.get(self.__class__),
            self.hidden,
            self.inherit_checks,
        )

    @property
    @abc.abstractmethod
    def implements(self) -> t.Sequence[t.Type[commands.Command]]:
        ...

    @property
    @abc.abstractmethod
    def name(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def description(self) -> str:
        ...

    @property
    def checks(self) -> t.Sequence[lightbulb.Check]:
        return []

    @property
    def aliases(self) -> t.Sequence[str]:
        return []

    @property
    def guilds(self) -> t.Union[int, t.Sequence[int], hikari.UNDEFINED]:
        return hikari.UNDEFINED

    @property
    def parser(self) -> t.Optional[t.Type[lightbulb.utils.BaseParser]]:
        return None

    @property
    def cooldown_manager(self) -> t.Optional[lightbulb.CooldownManager]:
        return None

    @property
    def auto_defer(self) -> bool:
        return False

    @property
    def ephemeral(self) -> bool:
        return False

    @property
    def hidden(self) -> bool:
        return False

    @property
    def inherit_checks(self) -> bool:
        return False

    async def callback(self, ctx: context.Context) -> None:
        pass

    @classmethod
    def child(
        cls, other: t.Optional[t.Type[CommandLike]] = None
    ) -> t.Union[t.Type[CommandLike], t.Callable[[t.Type[CommandLike]], t.Type[CommandLike]]]:
        if other is not None:
            CommandLike._subcommands[cls].append(other)
            return other

        def decorate(other_: t.Type[CommandLike]) -> t.Type[CommandLike]:
            CommandLike._subcommands[cls].append(other_)
            return other_

        return decorate
