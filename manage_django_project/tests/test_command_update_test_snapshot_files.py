from unittest.mock import patch

from django.test import SimpleTestCase
from manageprojects.test_utils.subprocess import SubprocessCallMock

from manage_django_project.management.commands import shell, update_test_snapshot_files
from manage_django_project.tests.cmd2_test_utils import BaseShellTestCase
from manage_django_project.tests.command_test_utils import EraseCoverageDataMixin, get_rstrip_paths


class ShellTestCase(BaseShellTestCase):
    def test_update_test_snapshot_files(self):
        with patch.object(shell, 'verbose_check_call') as call_mock:
            stdout, stderr = self.execute(command='update_test_snapshot_files')
        self.assertEqual(stderr, '')
        self.assertIn('call command manage_django_project.update_test_snapshot_files', stdout)
        call_mock.assert_called_once()


class CallTestCase(EraseCoverageDataMixin, SimpleTestCase):
    maxDiff = None

    def test_update_test_snapshot_files(self):
        command = update_test_snapshot_files.Command()

        class ProjectInfoMock:
            def __init__(self):
                self.config = self
                self.project_root_path = self

                self.rglob_calls = []
                self.unlink_calls = 0

            def rglob(self, pattern):
                self.rglob_calls.append(pattern)
                return [self]

            def unlink(self):
                self.unlink_calls += 1

        project_info_mock = ProjectInfoMock()
        with SubprocessCallMock() as call_mock, patch(
            'manage_django_project.management.commands.update_test_snapshot_files.project_info', project_info_mock
        ):
            try:
                command.run_from_argv(argv=[])
            except SystemExit as err:
                self.assertEqual(err.code, 0)

        self.assertEqual(
            project_info_mock.rglob_calls,
            [
                '*.snapshot.*',  # Collect for deleting
                '*.snapshot.*',  # Collect for info print
            ],
        )
        self.assertEqual(project_info_mock.unlink_calls, 1)

        # Just normal nox calls:
        popenargs = call_mock.get_popenargs(rstrip_paths=get_rstrip_paths())
        self.assertEqual(
            popenargs,
            [
                ['.../bin/nox'],
                ['.../bin/coverage', 'combine', '--append'],
                ['.../bin/coverage', 'report'],
                ['.../bin/coverage', 'xml'],
                ['.../bin/coverage', 'json'],
                ['.../bin/coverage', 'erase'],
            ],
        )
