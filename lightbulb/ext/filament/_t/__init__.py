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

__all__ = ["run"]

import pathlib
import typing as t

from nusex.api import template
from nusex.api import profile

if t.TYPE_CHECKING:
    from argparse import Namespace

PROFILE = profile.Profile(
    "default",
    author_name="tandemdude",
    author_email="tandemdude1@gmail.com",
    preferred_license="unlicense",
    starting_version="0.1.0",
)


def run(args: Namespace) -> None:
    tp = template.Template.from_disk(f"{args.style}_bot", from_dir=pathlib.Path(__file__[:-11]))
    tp.deploy(pathlib.Path("."), project_name=f"{args.style}_bot", profile=PROFILE)
