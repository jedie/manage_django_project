from bx_py_utils.environ import OverrideEnviron
from cli_base.cli_tools.dev_tools import is_verbose
from cli_base.cli_tools.test_utils.snapshot import UpdateTestSnapshotFiles

from manage_django_project.config import project_info
from manage_django_project.management.commands.nox import Command as BaseNoxCommand


class Command(BaseNoxCommand):
    help = 'Update all snapshot files (by remove and recreate all snapshot files)'

    def run_from_argv(self, argv):
        self.print_help_once()

        root_path = project_info.config.project_root_path
        verbose = is_verbose(argv=argv)

        with UpdateTestSnapshotFiles(root_path=root_path, verbose=verbose), OverrideEnviron(RAISE_SNAPSHOT_ERRORS='0'):
            # Run "nox" to recreate all snapshot files:
            super().run_from_argv(argv)
