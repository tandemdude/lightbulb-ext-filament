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


def opt(name: str, description: str, **kwargs: t.Any) -> commands.OptionLike:
    """
    Function that defines an option inside a command class. This function takes all the same
    arguments as :obj:`lightbulb.decorators.option`.

    Args:
        name (:obj:`str`): Name of the option.
        description (:obj:`str`): Description of the option.
        **kwargs: Additional keyword arguments passed to the :obj:`lightbulb.decorators.option` decorator.

    Returns:
        :obj:`lightbulb.commands.base.OptionLike`: Created option object.
    """
    kwargs.setdefault("required", kwargs.get("default", hikari.UNDEFINED) is hikari.UNDEFINED)
    if not kwargs["required"]:
        kwargs.setdefault("default", None)
    return commands.OptionLike(name, description, **kwargs)


option = opt
"""Alias for :obj:`~opt`."""


class CommandLike(abc.ABC):
    """
    Base class for filament's command implementation. All of your command's must
    be a subclass of this.
    """

    _subcommands: t.Dict[t.Type[CommandLike], t.List[t.Type[CommandLike]]] = collections.defaultdict(list)
    _error_handlers: t.Dict[t.Type[CommandLike], t.Callable[[context.Context], t.Coroutine[t.Any, t.Any, bool]]] = {}
    _help_getters: t.Dict[t.Type[CommandLike], t.Callable[[commands.Command, context.Context], str]] = {}
    _check_exempts: t.Dict[
        t.Type[CommandLike], t.Callable[[context.Context], t.Union[bool, t.Coroutine[t.Any, t.Any, bool]]]
    ] = {}

    def __new__(cls, *args: t.Any, **kwargs: t.Any) -> commands.CommandLike:
        new = super().__new__(cls, *args, **kwargs)
        # Turn the created filament CommandLike into a lightbulb CommandLike so it can
        # actually be added to the bot
        return new._as_lightbulb_commandlike()

    def _find_options(self) -> t.MutableMapping[str, commands.OptionLike]:
        options = {}
        # Search through the class' attributes to find all defined options
        for item in dir(self):
            obj = getattr(self, item)
            if isinstance(obj, commands.OptionLike):
                options[obj.name] = obj
        return options

    def _as_lightbulb_commandlike(self) -> commands.CommandLike:
        # We need to wrap the callback here so that we can set the __cmd_types__ attribute
        # in order for lightbulb to be able to detect what command types to create
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
        """
        Sequence of the lightbulb command types that this command class will implement.
        """
        ...

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """
        The name of this command.
        """
        ...

    @property
    @abc.abstractmethod
    def description(self) -> str:
        """
        The description of this command.
        """
        ...

    @property
    def checks(self) -> t.Sequence[lightbulb.Check]:
        """
        Sequence of checks to user for this command.
        """
        return []

    @property
    def aliases(self) -> t.Sequence[str]:
        """
        Sequence of aliases to use for this command. This only applies to prefix commands.
        """
        return []

    @property
    def guilds(self) -> t.Union[int, t.Sequence[int], hikari.UNDEFINED]:
        """
        Guild ID or IDs to restrict this command to. This only applies to application commands.
        """
        return hikari.UNDEFINED

    @property
    def parser(self) -> t.Optional[t.Type[lightbulb.utils.BaseParser]]:
        """
        The argument parser class to use for this command. If not specified :obj:`lightbulb.utils.parser.Parser`
        will be used. Only applies to prefix commands.
        """
        return None

    @property
    def cooldown_manager(self) -> t.Optional[lightbulb.CooldownManager]:
        """
        The cooldown manager instance to use for this command.
        """
        return None

    @property
    def auto_defer(self) -> bool:
        """
        Whether or not a deferred response should be automatically created for invocations of this command.
        """
        return False

    @property
    def ephemeral(self) -> bool:
        """
        Whether or not responses from this command should be ephemeral by default. Only applies to
        application commands.
        """
        return False

    @property
    def hidden(self) -> bool:
        """
        Whether or not this command should be hidden from the default help command.
        """
        return False

    @property
    def inherit_checks(self) -> bool:
        """
        Whether or not this command should inherit checks from its parent command. Only applies to subcommands.
        """
        return False

    async def callback(self, ctx: context.Context) -> None:
        """
        The callback function for this command - called when the command is invoked.

        Args:
            ctx (:obj:`lightbulb.context.base.Context`): The context that the command was invoked under.

        Returns:
            ``None``
        """
        pass

    @classmethod
    def child(
        cls, other: t.Optional[t.Type[CommandLike]] = None
    ) -> t.Union[t.Type[CommandLike], t.Callable[[t.Type[CommandLike]], t.Type[CommandLike]]]:
        """
        Registers a :obj:`~CommandLike` subclass as a child to this command.
        This can be used as a first or second order decorator, or called manually with the :obj:`~CommandLike`
        subclass to add as a child.
        """
        if other is not None:
            CommandLike._subcommands[cls].append(other)
            return other

        def decorate(other_: t.Type[CommandLike]) -> t.Type[CommandLike]:
            CommandLike._subcommands[cls].append(other_)
            return other_

        return decorate
