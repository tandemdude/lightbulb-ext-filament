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
An alternative, decorator-based implementation of slash commands as opposed to the class-based
system provided by hikari-lightbulb.

**Currently supported:**

- Top level slash commands
- Slash command options
- Slash command checks

**Support planned:**

- Slash command groups
- Slash command subgroups
- Slash command subcommands
"""
from filament.slash_commands import decorators
from filament.slash_commands.decorators import *

__all__ = [
    *decorators.__all__,
]
