import ast
import contextlib
import io
import re
import sys
import textwrap
import time
import typing
import traceback

import lightbulb

__all__: typing.Final[typing.List[str]] = ["SuperUser", "load", "unload"]


CODEBLOCK_REGEX: typing.Final[typing.Pattern[str]] = re.compile(
    r"```(?P<lang>[a-zA-Z0-9]*)\s(?P<code>[\s\S(^\\`{3})]*?)\s*```"
)
LANGUAGES: typing.Final[typing.Mapping[str, str]] = {
    "": "python",
    "py": "python",
    "python": "python",
    "python3": "python",
    "py3": "python",
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
                    abstract_syntax_tree = ast.parse(
                        code, filename=f"{ctx.guild_id}_{ctx.channel_id}.py"
                    )

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


class SuperUser(lightbulb.Plugin):
    @lightbulb.owner_only()
    @lightbulb.command(name="exec", aliases=["eval"])
    async def _exec(self, ctx: lightbulb.Context, *, code: str):
        if code.startswith("```"):
            match = CODEBLOCK_REGEX.match(code)
            lang, code = LANGUAGES[match.group("lang")], match.group("code")
        else:
            lang = "python"

        sout, serr, result, exec_time, prog = await execute_in_session(ctx, lang, code)

        pag = lightbulb.utils.StringPaginator(prefix="```diff\n", suffix="```")

        pag.add_line(f"---- {prog} ----")
        if sout:
            pag.add_line("- /dev/stdout:")
            pag.add_line(sout)
        if serr:
            pag.add_line("- /dev/stderr:")
            pag.add_line(serr)
        pag.add_line(f"+ Returned {result} in approx {(exec_time*1000):.2f}ms")

        nav = lightbulb.utils.StringNavigator(pag.build_pages())
        await nav.run(ctx)


def load(bot: lightbulb.Bot):
    bot.add_plugin(SuperUser())


def unload(bot: lightbulb.Bot):
    bot.remove_plugin("SuperUser")
