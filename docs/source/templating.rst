==========
Templating
==========

Filament, when run through the command line, allows the generation of template projects using either the lightbulb decorator-based
command system, or the filament class-based command system. To generate a template project you should run the below command
in the directory of your choice:

.. code-block:: bash

   python -m lightbulb.ext.filament -n

This command will create a template using lightbulb's decorator-based command system. If you would rather use filament's
class-based command system you should run the command with an additional argument: ``-s filament``. This means the command
would be as follows:

.. code-block:: bash

   python -m lightbulb.ext.filament -n -s filament

The above commands will create a project with the following structure:

.. code-block::

    bot/
    ├─ exts/
    │  ├─ __init__.py
    │  ├─ ping.py
    ├─ __init__.py
    ├─ __main__.py
    ├─ bot.py
    token.txt

To run the bot, you should copy-paste your bot's token into the ``token.txt`` file, replacing any text that is already
present, then run the command `python -m bot` in the root of your project. The bot should then come online. You can verify
that the bot is working correctly by running the ``!ping`` command.
