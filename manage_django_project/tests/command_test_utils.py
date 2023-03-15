import inspect
import os
import sys
from pathlib import Path

import rich
from django.core.management import call_command
from manageprojects.test_utils.subprocess import SubprocessCallMock

from manage_django_project.tests import PROJECT_ROOT


def get_rstrip_paths():
    return (
        Path(sys.executable).parent.parent,
        PROJECT_ROOT.parent,
    )


def call_command_capture_subprocess(cmd_module, direct_call=False) -> list[str]:
    assert inspect.ismodule(cmd_module)

    command = cmd_module.Command()

    with SubprocessCallMock() as call_mock:
        if direct_call:
            command.run_from_argv(argv=(sys.executable, cmd_module.__name__))
        else:
            call_command(command)

    popenargs = call_mock.get_popenargs(rstrip_paths=get_rstrip_paths())
    return popenargs


class ForceRichTerminalWidth:
    def __init__(self, width=120):
        self.width = width
        self.origin_width = None

    def __enter__(self):
        console = rich.get_console()
        self.origin_width = console.width
        os.environ['COLUMNS'] = str(self.width)
        rich.reconfigure(width=self.width)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            return False
        rich.reconfigure(width=self.origin_width)
        os.environ['COLUMNS'] = str(self.origin_width)
