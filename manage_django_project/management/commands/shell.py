from __future__ import annotations

import logging
import os
import sys
from importlib import import_module

import cmd2
from cli_base.cli_tools.subprocess_utils import verbose_check_call
from cmd2 import Statement, categorize
from cmd2.constants import CMD_ATTR_ARGPARSER, CMD_ATTR_PRESERVE_QUOTES
from cmd2.decorators import _set_parser_prog
from django.core.management import BaseCommand, CommandParser, get_commands
from rich import get_console, print
from rich.console import Console
from rich.panel import Panel

from manage_django_project.config import project_info
from manage_django_project.management.base import BasePassManageCommand


logger = logging.getLogger(__name__)


class DjangoCommand:
    def __init__(self, *, command_name, package_name, console: Console):
        self.command_name = command_name
        self.package_name = package_name
        self.console = console

    def __call__(self, statement: Statement):
        """
        Call the Django command.
        Don't use django.core.management.call_command() because we can't switch the needed Django settings.
        """
        verbose = statement.args != '--help'

        if verbose:
            self.console.print(
                Panel(f'[magenta]call command[/magenta] [cyan]{self.package_name}.[bold]{self.command_name}')
            )

        # call our manage_django_project.manage.execute_django_from_command_line()
        # and pass all arguments
        args = [sys.executable, '-m', project_info.config.module.__name__, self.command_name]
        if arg_list := statement.arg_list:
            args.extend(arg_list)

        # Don't force any settings:
        env = {k: v for k, v in os.environ.items() if k != 'DJANGO_SETTINGS_MODULE'}

        verbose_check_call(
            *args,
            verbose=verbose,
            env=env,
            timeout=None,  # No default timeout -> run forever
        )


class ManageDjangoProjectApp(cmd2.Cmd):
    # Remove some default cmd2 commands:
    delattr(cmd2.Cmd, 'do_edit')
    delattr(cmd2.Cmd, 'do_shell')
    delattr(cmd2.Cmd, 'do_run_script')
    delattr(cmd2.Cmd, 'do_run_pyscript')

    def __init__(self, *args, console: Console | None = None, **kwargs):
        if not console:
            self.console = get_console()
        else:
            self.console = console

        for command_name, app_name in get_commands().items():
            if command_name == 'shell':
                continue

            pkg_name = f'{app_name}.management.commands.{command_name}'
            try:
                module = import_module(pkg_name)
            except Exception as err:
                msg = f'Error import "{pkg_name}": {err}'
                logger.exception(msg)
                print(f'[red]{msg}')
                continue

            try:
                CommandClass = module.Command
            except AttributeError as err:
                logger.info('Skip %s because of: %s', pkg_name, err)
                continue

            try:
                assert issubclass(CommandClass, BaseCommand)
            except AssertionError as err:
                logger.info('Skip %s because of: %s', pkg_name, err)
                continue

            try:
                cmd_instance: BaseCommand = CommandClass()
            except Exception as err:
                msg = f'Error make instance of "{pkg_name}": {err}'
                logger.exception(msg)
                print(f'[red]{msg}')
                continue

            cmd = DjangoCommand(command_name=command_name, package_name=app_name, console=self.console)

            categorize(func=cmd, category=app_name)

            parser: CommandParser = cmd_instance.create_parser(prog_name='manage.py', subcommand=command_name)

            _set_parser_prog(parser, prog='./manage.py')

            cmd.__doc__ = CommandClass.help

            setattr(cmd, CMD_ATTR_ARGPARSER, parser)
            setattr(cmd, CMD_ATTR_PRESERVE_QUOTES, False)

            setattr(self, f'do_{command_name}', cmd)

        super().__init__(*args, stdout=self.console.file, **kwargs)

        self._startup_commands = ['help']

        # Set aliases:
        self.aliases.update({'q': 'quit'})

        # Display Tracebacks on errors:
        self.debug = True

        self.prompt = f'\n({project_info.distribution_name}) '


class Command(BasePassManageCommand):
    help = 'Go into cmd2 shell with all registered Django manage commands'

    def run_from_argv(self, argv):
        super().run_from_argv(argv)

        app = ManageDjangoProjectApp(console=self.console)
        app.cmdloop()
