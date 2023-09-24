from bx_py_utils.environ import OverrideEnviron
from rich import print

from manage_django_project.config import project_info
from manage_django_project.management.commands.tox import Command as BaseToxCommand


def delete_snapshot_files(verbose=True):
    """Delete all snapshot files"""
    cwd = project_info.config.project_root_path
    unlink_count = 0
    for snapshot_path in cwd.rglob('*.snapshot.*'):
        snapshot_path.unlink()
        unlink_count += 1
    if verbose:
        print(f'[green]Delete {unlink_count} snapshot files')


class Command(BaseToxCommand):
    help = 'Update all snapshot files (by remove and recreate all snapshot files)'

    def run_from_argv(self, argv):
        self.print_help_once()
        delete_snapshot_files()
        with OverrideEnviron(RAISE_SNAPSHOT_ERRORS='0'):
            # Run "tox" to recreate all snapshot files:
            super().run_from_argv(argv)
