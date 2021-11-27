=====================
General API Reference
=====================

Commands
========

Filament provides a different method of defining commands than is provided by lightbulb. It uses a class-based
approach similar to how slash commands were defined in lightbulb v1.

To create commands you need to subclass :obj:`filament.commands.impl.CommandLike` and define class
attributes in order to specify parameters such as command name, description, etc.

Example:

.. code-block:: python

    import lightbulb
    from lightbulb import commands
    import filament

    class EchoCommand(filament.CommandLike):
        # This defines the command types that this command will implement
        # Similar to the @lightbulb.implements decorator for lightbulb commands
        implements = [commands.SlashCommand, commands.PrefixCommand]

        # Define the command's name
        name = "echo"
        # Define the command's description
        description = "Repeats the input text

        # Define 0 or more options for the command. In this case we will have a single
        # string option
        text_opt = filament.opt("text", "Text to repeat", modifier=commands.OptionModifier.CONSUME_REST)

        # Define the callback function for this command
        async def callback(self, ctx: lightbulb.context.Context) -> None:
            await ctx.respond(ctx.options.text)

You are **required** to override the following attributes:

- :obj:`filament.commands.impl.CommandLike.implements`

- :obj:`filament.commands.impl.CommandLike.name`

- :obj:`filament.commands.impl.CommandLike.description`

- :obj:`filament.commands.impl.CommandLike.callback` (if you actually want the command to do something)

There are also some attributes available that you can override for additional functionality:

- :obj:`filament.commands.impl.CommandLike.checks`

- :obj:`filament.commands.impl.CommandLike.aliases`

- :obj:`filament.commands.impl.CommandLike.guilds` (recommended, unless you want your application commands to be global, you
  can also specify a value for :obj:`lightbulb.app.BotApp.default_enabled_guilds` instead of specifying a value here)

- :obj:`filament.commands.impl.CommandLike.parser`

- :obj:`filament.commands.impl.CommandLike.cooldown_manager`

- :obj:`filament.commands.impl.CommandLike.auto_defer`

- :obj:`filament.commands.impl.CommandLike.ephemeral`

- :obj:`filament.commands.impl.CommandLike.hidden`

- :obj:`filament.commands.impl.CommandLike.inherit_checks`

----

Command Groups and Subcommands
==============================

Creating groups and subcommands is relatively simple. You need to first create a command that implements a command group:

.. code-block:: python

    from lightbulb import commands
    import filament

    class FooGroup(filament.CommandLike):
        # Define that this command implements SlashCommandGroup
        implements = [commands.SlashCommandGroup]
        # The command's name
        name = "foo"
        # The command's description
        description = "test command group"
        # Note that we don't need to override the callback here because due to a discord limitation,
        # slash command groups cannot be invoked.

To create a subcommand for the above group, we create a second command class and mark it as a child of ``FooGroup``. The
subcommand class **must** implement the appropriate command type, which in this case is :obj:`lightbulb.commands.slash.SlashSubCommand`:

.. code-block:: python

    import lightbulb
    from lightbulb import commands
    import filament

    @FooGroup.child
    class BarSubcommand(filament.CommandLike):
        # Define that this command implements SlashSubCommand
        implements = [commands.SlashSubCommand]
        # The command's name
        name = "bar"
        # The command's description
        description = "test subcommand"

        async def callback(self, ctx: lightbulb.context.Context) -> None:
            # Just send a simple message to the invocation context so we know the command worked
            await ctx.respond("foo bar")

----

API Reference
=============

.. automodule:: filament.commands.impl
    :members:
