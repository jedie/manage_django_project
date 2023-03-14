from cmd2 import CommandResult
from cmd2.ansi import strip_style
from cmd2_ext_test import ExternalTestMixin
from django.test import SimpleTestCase

from manage_django_project.management.commands.shell import ManageDjangoProjectApp


class ManageDjangoTestApp(ExternalTestMixin, ManageDjangoProjectApp):
    pass


class BaseShellTestCase(SimpleTestCase):
    """
    Base class for cmd2 app test cases
    """

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
