==========
Extensions
==========

Superuser
=========

This extension provides commands to allow you to run arbitrary python and shell code through the bot, as well
as checking the output of the run code.

The commands in this extension are restricted to only be usable by the bot's owner(s) as running arbitrary code
is fundamentally unsafe.

**Commands Provided:**

- ``exec`` (aliases: ``eval``, ``shell``, ``sh``)
- ``shell`` (alias of exec, but runs code in the shell by default instead of using python)

**How to Load:**

.. code-block:: python

    bot.load_extensions("filament.exts.superuser")
