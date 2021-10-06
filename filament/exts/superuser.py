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
import ast
import asyncio
import contextlib
import io
import os
import re
import shutil
import sys
import textwrap
import time
import traceback
import typing

import lightbulb

__all__: typing.Final[typing.List[str]] = ["SuperUser", "load", "unload"]

SHELL = os.getenv("SHELL", os.name in ("win32", "win64", "winnt", "nt") and "cmd" or "bash")
CODEBLOCK_REGEX: typing.Final[typing.Pattern[str]] = re.compile(
    r"```(?P<lang>[a-zA-Z0-9]*)\s(?P<code>[\s\S(^\\`{3})]*?)\s*```"
)
LANGUAGES: typing.Final[typing.Mapping[str, str]] = {
    "": "python",
    "py": "python",
    "python": "python",
    "python3": "python",
    "py3": "python",
    "shell": SHELL,
    "sh": SHELL,
    "bash": SHELL,
}


async def execute_in_session(ctx: lightbulb.Context, program: str, code: str):
    sout = io.StringIO()
    serr = io.StringIO()

    nl = "\n"

    with contextlib.redirect_stdout(sout):
        with contextlib.redirect_stderr(serr):

            start_time = float("nan")
            try:
                try:
                    abstract_syntax_tree = ast.parse(code, filename=f"{ctx.guild_id}_{ctx.channel_id}.py")

                    node: list = abstract_syntax_tree.body

                    if node and type(node[0]) is ast.Expr:
                        code = f"return " + code.strip()

                except Exception:
                    pass

                func = f"async def aexec(ctx, bot):\n{textwrap.indent(code, '    ')}"

                start_time = time.monotonic()
                exec(func, globals(), locals())

                result = await locals()["aexec"](ctx, ctx.bot)
                if hasattr(result, "__await__"):
                    print(f"Returned awaitable {result}. Awaiting it.", file=sys.stderr)
                    result = await result
            except BaseException as ex:
                traceback.print_exc()
                result = type(ex)
            finally:
                exec_time = time.monotonic() - start_time

    return (
        sout.getvalue(),
        serr.getvalue(),
        result,
        exec_time,
        f'Python {sys.version.replace(nl, " ")}',
    )


async def execute_in_shell(_: lightbulb.Context, program: str, code: str):
    path = shutil.which(program)
    if not path:
        return "", f"{program} not found.", 127, 0.0, ""

    start_time = time.monotonic()
    process = await asyncio.create_subprocess_exec(
        path,
        "--",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.PIPE,
    )

    sout, serr = await process.communicate(bytes(code, "utf-8"))
    exec_time = time.monotonic() - start_time

    exit_code = process.returncode

    sout = sout.decode()
    serr = serr.decode()

    return sout, serr, str(exit_code), exec_time, path


class SuperUser(lightbulb.Plugin):
    def __init__(self):
        super().__init__()

    def _paginate_output(self, pag, sout, serr, result, exec_time, prog):
        pag.add_line(f"---- {prog} ----")
        if sout:
            pag.add_line("- /dev/stdout:")
            pag.add_line(sout)
        if serr:
            pag.add_line("- /dev/stderr:")
            pag.add_line(serr)
        pag.add_line(f"+ Returned {result} in approx {(exec_time * 1000):.2f}ms")

    @lightbulb.check(lightbulb.owner_only)
    @lightbulb.command(name="exec", aliases=["eval", "shell", "sh"])
    async def execute(self, ctx: lightbulb.Context, *, code: str):
        if code.startswith("```"):
            match = CODEBLOCK_REGEX.match(code)
            lang, code = LANGUAGES[match.group("lang")], match.group("code")
        else:
            if ctx.invoked_with in ["shell", "sh"]:
                lang = SHELL
            else:
                lang = "python"

        executor = execute_in_session if lang == "python" else execute_in_shell
        sout, serr, result, exec_time, prog = await executor(ctx, lang, code)

        pag = lightbulb.utils.StringPaginator(prefix="```diff\n", suffix="```")
        self._paginate_output(pag, sout, serr, result, exec_time, prog)
        nav = lightbulb.utils.StringNavigator(pag.build_pages())
        await nav.run(ctx)


def load(bot: lightbulb.Bot):
    bot.add_plugin(SuperUser())


def unload(bot: lightbulb.Bot):
    bot.remove_plugin("SuperUser")
