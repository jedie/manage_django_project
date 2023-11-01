from importlib import import_module
from pathlib import Path

from bx_py_utils.auto_doc import assert_readme_block
from bx_py_utils.path import assert_is_file
from cli_base.cli_tools.git_history import get_git_history
from django.test import SimpleTestCase

import manage_django_project
from manage_django_project.management import commands
from manage_django_project.tests import PROJECT_ROOT


def get_own_command_names() -> list[str]:
    commands_path = Path(commands.__file__).parent
    command_names = [item.stem for item in commands_path.glob('*.py') if not item.stem.startswith('_')]
    return command_names


def get_own_commands():
    command_names = get_own_command_names()
    result = {}
    for command_name in command_names:
        module = import_module(f'manage_django_project.management.commands.{command_name}')
        CommandClass = module.Command
        result[command_name] = CommandClass

    return result


def assert_cli_help_in_readme(text_block: str, marker: str):
    README_PATH = PROJECT_ROOT / 'README.md'
    assert_is_file(README_PATH)

    assert_readme_block(
        readme_path=README_PATH,
        text_block=text_block,
        start_marker_line=f'[comment]: <> (✂✂✂ auto generated {marker} start ✂✂✂)',
        end_marker_line=f'[comment]: <> (✂✂✂ auto generated {marker} end ✂✂✂)',
    )


class ReadmeTestCase(SimpleTestCase):
    def test_own_commands(self):
        commands = get_own_commands()
        self.assertGreaterEqual(len(commands), 10)
        help_info = []
        for command_name, CommandClass in sorted(commands.items()):
            if help := CommandClass.help:
                help_info.append(f'* `{command_name}` - {help}')
        help_info = '\n'.join(help_info)
        text_block = f'\n{help_info}\n'
        assert_cli_help_in_readme(text_block=text_block, marker='command_info')

    def test_readme_history(self):
        git_history = get_git_history(
            current_version=manage_django_project.__version__,
            add_author=False,
        )
        history = '\n'.join(git_history)
        assert_readme_block(
            readme_path=PROJECT_ROOT / 'README.md',
            text_block=f'\n{history}\n',
            start_marker_line='[comment]: <> (✂✂✂ auto generated history start ✂✂✂)',
            end_marker_line='[comment]: <> (✂✂✂ auto generated history end ✂✂✂)',
        )
