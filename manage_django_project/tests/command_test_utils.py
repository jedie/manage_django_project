import inspect
import sys
import unittest
from pathlib import Path

from django.core.management import call_command
from manageprojects.test_utils.subprocess import SimpleRunReturnCallback, SubprocessCallMock

from manage_django_project.management.commands.coverage import erase_coverage_data
from manage_django_project.tests import PROJECT_ROOT


def get_rstrip_paths():
    return (
        Path(sys.executable).parent.parent,
        PROJECT_ROOT.parent,
    )


def call_command_capture_subprocess(cmd_module) -> list:
    assert inspect.ismodule(cmd_module)

    with SubprocessCallMock(return_callback=SimpleRunReturnCallback(stdout='mocked output')) as call_mock:
        try:
            call_command(cmd_module.Command())
        except SystemExit:
            # some commands may call sys.exit()
            pass

    popenargs = call_mock.get_popenargs(rstrip_paths=get_rstrip_paths())
    return popenargs


class EraseCoverageDataMixin(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        erase_coverage_data.erased = False

    def tearDown(self) -> None:
        super().tearDown()
        erase_coverage_data.erased = False
