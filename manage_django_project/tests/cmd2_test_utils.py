from __future__ import annotations

import dataclasses
import inspect
import io

from cmd2 import CommandResult
from cmd2.ansi import strip_style
from cmd2_ext_test import ExternalTestMixin
from django.core.management import BaseCommand
from django.test import SimpleTestCase
from django_tools.unittest_utils.stdout_redirect import DenyStdWrite

from manage_django_project.management.commands.shell import ManageDjangoProjectApp


class ManageDjangoTestApp(ExternalTestMixin, ManageDjangoProjectApp):
    pass


class BaseShellTestCase(SimpleTestCase):
    """
    Base class for cmd2 app test cases
    """

    maxDiff = 2000

    def setUp(self):
        super().setUp()
        self.app = ManageDjangoTestApp()
        self.app.fixture_setup()

    def tearDown(self):
        super().tearDown()
        self.app.fixture_teardown()

    def execute(self, command, remove_colors=True, rstrip=True):
        out = self.app.app_cmd(command)

        assert isinstance(out, CommandResult)
        if out.stdout is None:
            stdout = ''
        else:
            stdout = str(out.stdout)
            if remove_colors:
                stdout = strip_style(stdout)
            if rstrip:
                stdout = '\n'.join(line.rstrip() for line in stdout.splitlines())

        if out.stderr is None:
            stderr = ''
        else:
            stderr = str(out.stderr)
            if remove_colors:
                stderr = strip_style(stderr)

        return stdout, stderr


class Buffer(io.StringIO):
    def __repr__(self):
        return '<captured_call_command StringIO buffer>'


@dataclasses.dataclass
class Result:
    exit_code: int | None
    stdout: str
    stderr: str


def run_command_from_argv(command, argv: list) -> Result:
    """
    Call django manage command via `run_from_argv()` and return stdout + stderr
    """
    try:
        assert inspect.ismodule(command)
        CommandClass = command.Command
        assert issubclass(CommandClass, BaseCommand)
    except Exception as err:
        raise AssertionError(f'{command!r} is no Django Management command: {err}')

    command_name = command.__name__
    command_name = command_name.rsplit('.', 1)[-1]

    capture_stdout = Buffer()
    capture_stderr = Buffer()

    command_instance = CommandClass(
        stdout=capture_stdout,
        stderr=capture_stderr,
        no_color=True,
        force_color=False,
    )

    with DenyStdWrite(name=command_name):
        try:
            command_instance.run_from_argv(argv)
        except SystemExit as err:
            exit_code = err.code
        else:
            exit_code = None

    return Result(
        exit_code=exit_code,
        stdout=capture_stdout.getvalue(),
        stderr=capture_stderr.getvalue(),
    )
