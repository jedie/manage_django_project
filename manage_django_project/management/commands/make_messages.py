import os
import sys
from pathlib import Path

from cli_base.cli_tools.git import Git
from django.core.management import BaseCommand, call_command
from django.core.management.commands import compilemessages, makemessages

from manage_django_project.config import project_info


class Command(BaseCommand):
    help = 'Make and compile locales message files'

    def handle(self, *args, **options):
        self.stdout.write()
        self.stdout.write('=' * 100)
        self.stdout.write(self.help)
        self.stdout.write('-' * 100)

        verbosity = options.get('verbosity', 1)

        root_path = project_info.config.project_root_path
        if verbosity:
            self.stdout.write(f'Scan git tracked files in project root: {root_path}')

        git = Git(cwd=root_path, detect_root=True)

        locale_parent_paths = set()
        for file_path in git.ls_files():
            if not file_path.name.endswith('.po'):
                continue

            if locale_pos := file_path.parts.index('locale'):
                if locale_parent_path := file_path.parts[:locale_pos]:
                    locale_parent_paths.add(Path(*locale_parent_path))

        if not locale_parent_paths:
            self.stderr.write('No locale files found in git tracked files.')
            sys.exit(1)

        cwd = Path.cwd()

        for locale_path in sorted(locale_parent_paths):
            self.stdout.write('_' * 100)
            self.stdout.write(f'Process locale path: {locale_path.relative_to(cwd)}')

            os.chdir(locale_path)

            self.stdout.write('\nMake messages...')
            call_command(
                makemessages.Command(),
                **self.get_make_messages_kwargs(),
                verbosity=verbosity,
            )
            self.stdout.write('\nCompile messages...')
            call_command(
                compilemessages.Command(),
                **self.get_compile_messages_kwargs(),
                verbosity=verbosity,
            )

    def get_make_messages_kwargs(self):
        return dict(
            all=True,
            no_location=True,
            no_obsolete=True,
            ignore=['.*', 'htmlcov', 'volumes'],
        )

    def get_compile_messages_kwargs(self):
        return dict(
            fuzzy=False,
        )
