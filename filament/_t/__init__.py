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
from unittest import mock

from nusex import constants
from nusex.cli.commands import deploy

if t.TYPE_CHECKING:
    from argparse import Namespace

PLACEHOLDER_DATA = {
    "starting_version": "0.1.0",
    "default_description": "Simple template for a hikari-lightbulb discord bot.",
    "git_profile_url": "https://github.com/tandemdude",
    "author_email": "tandemdude1@gmail.com",
    "author_name": "tandemdude",
    "preferred_license": "unlicense",
}


def run(args: Namespace) -> None:
    """
    This is an evil hack to get nusex to deploy the template without first initialising nusex
    and without any of the files being in the correct directories.
    """
    # We need to mock Profile out of nusex so we can replace the profile's data with our own
    # so that nusex will run deploy without it first being initialised
    with mock.patch("nusex.template.Profile") as mock_profile:
        mock_profile.return_value = mock_profile
        mock_profile.current.return_value = PLACEHOLDER_DATA

        # Change the directories to our local template directory because nusex init takes too long
        constants.LICENSE_DIR = pathlib.Path(".")
        constants.TEMPLATE_DIR = pathlib.Path(".")

        deploy.run(f"{args.style}_bot", f"{args.style}_bot", False, True)
