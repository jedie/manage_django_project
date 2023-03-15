import inspect

from django.core.management import call_command
from manageprojects.test_utils.subprocess import SubprocessCallMock

from manage_django_project.tests import PROJECT_ROOT


def call_command_capture_subprocess(cmd_module) -> list[str]:
    assert inspect.ismodule(cmd_module)

    with SubprocessCallMock() as call_mock:
        call_command(cmd_module.Command())

    popenargs = call_mock.get_popenargs(rstrip_paths=(PROJECT_ROOT,))
    return popenargs
