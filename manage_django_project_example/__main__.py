"""
    Allow manage_django_project to be executable
    through `python -m manage_django_project`.
"""
from pathlib import Path

import manage_django_project_example
from manage_django_project.config import ManageConfig
from manage_django_project.manage import execute_django_from_command_line


def main():
    """
    entrypoint installed via pyproject.toml and [project.scripts] section.
    Must be set in ./manage.py and PROJECT_SHELL_SCRIPT
    """
    execute_django_from_command_line(
        config=ManageConfig(
            module=manage_django_project_example,
            #
            # Path that contains your `pyproject.toml`:
            project_root_path=Path(manage_django_project_example.__file__).parent.parent,
            #
            # Django settings used for all commands except test/coverage/tox:
            local_settings='manage_django_project_example.settings.local',
            #
            # Django settings used for test/coverage/tox commands:
            test_settings='manage_django_project_example.settings.tests',
        )
    )


if __name__ == '__main__':
    main()
