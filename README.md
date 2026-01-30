<h1>
  <img src="https://raw.githubusercontent.com/jedie/manage_django_project/main/manage_django_project/static/manage_django_project.svg" width="32px" alt="Logo">
  manage_django_project
</h1>

[![tests](https://github.com/jedie/manage_django_project/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/jedie/manage_django_project/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/manage_django_project/branch/main/graph/badge.svg)](https://app.codecov.io/github/jedie/manage_django_project)
[![manage_django_project @ PyPi](https://img.shields.io/pypi/v/manage_django_project?label=manage_django_project%20%40%20PyPi)](https://pypi.org/project/manage_django_project/)
[![Python Versions](https://img.shields.io/pypi/pyversions/manage_django_project)](https://github.com/jedie/manage_django_project/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/manage_django_project)](https://github.com/jedie/manage_django_project/blob/main/LICENSE)

Helper to develop Django projects:

* Easy bootstrap a virtual environment:
  * Just get the sources and call `./manage.py`
  * Only `python3-pip` and `python3-venv` package needed to bootstarp
* Alle Django manage commands useable as normal CLI **and** via `cmd2` shell
* `cmd2` shell with autocomplete of all existing manage commands and all options
* Auto switching Django settings between `local` and `tests` settings.
* Helpful manage commands for developing:

### Included Django management commands:

[comment]: <> (✂✂✂ auto generated command_info start ✂✂✂)

* `code_style` - Check/Fix project code style
* `coverage` - Run tests with coverage and report
* `install` - Just install the project as editable via pip (Useful if version has been changed)
* `make_messages` - Make and compile locales message files
* `nox` - Run tests via nox
* `pip_audit` - Run `pip-audit` with configuration from `pyproject.toml`
* `playwright` - Call playwright CLI
* `project_info` - Information about the current Django project
* `publish` - Build a new release and publish it to PyPi
* `run_dev_server` - Setup test project and run django developer server
* `shell` - Go into cmd2 shell with all registered Django manage commands
* `update_req` - Update project requirements via uv
* `update_test_snapshot_files` - Update all snapshot files (by remove and recreate all snapshot files)

[comment]: <> (✂✂✂ auto generated command_info end ✂✂✂)


## How to use it

Some steps are needed to use `manage_django_project` in your project.

Here a overview and below details:

* add `manage_django_project` to your dev dependencies
* You Django project should have separate settings for `prod`, `local` and `tests` (Last two ones are used by `manage_django_project`)
* Add the bootstrap `manage.py`
* Add a `__main__.py` with the `execute_django_from_command_line()` call.
* In your `pyproject.toml`:
  * Add the `[manage_django_project]` section
  * Add the `__main__`-file as `[project.scripts]`
* Add the name of your `[project.scripts]` into bootstrap `manage.py`

All examples below used `manage_django_project_example`. You have to rename this string/path to your Django package name.

Full example is here: https://github.com/jedie/manage_django_project/tree/main/manage_django_project_example


If everything works as expected you can just call the `./manage.py` file and the magic happens ;)


### __main__.py

Add a `.../manage_django_project_example/__main__.py` file, looks like:

```python
from manage_django_project.manage import execute_django_from_command_line


def main():
    """
    entrypoint installed via pyproject.toml and [project.scripts] section.
    Must be set in ./manage.py and PROJECT_SHELL_SCRIPT
    """
    execute_django_from_command_line()


if __name__ == '__main__':
    main()
```


### pyproject.toml

```toml
[project.scripts]
manage_django_project_example = "manage_django_project_example.__main__:main"

[manage_django_project]
module_name="your_project_example"

# Django settings used for all commands except test/coverage/nox:
local_settings='your_project.settings.local'

# Django settings used for test/coverage/nox commands:
test_settings='your_project.settings.tests'
```


### ./manage.py

Add a copy of [manage.py](https://github.com/jedie/manage_django_project/blob/main/manage.py) file to your project source root.

Change only `manage_django_project_example` in this line:
```python
PROJECT_SHELL_SCRIPT = BIN_PATH / 'manage_django_project_example'
```


## Start hacking

Just clone the project and start `./manage.py` to bootstrap a virtual environment:

```bash
# Install base requirements:
~$ sudo apt install python3-pip python3-venv

# Get the sources:
~$ git clone https://github.com/jedie/manage_django_project.git
~$ cd manage_django_project/

# Just call manage.py and the magic happen:
~/manage_django_project$ ./manage.py

# start local dev. web server:
~/django-for-runners$ ./manage.py run_dev_server

# run tests:
~/django-for-runners$ ./manage.py test
# or with coverage
~/django-for-runners$ ./manage.py coverage
# or via nox:
~/django-for-runners$ ./manage.py nox
```


## Backwards-incompatible changes

### v0.2.x -> v0.3.x

The config was moved out from `__main__.py` into `pyproject.toml`

You must add in your `pyproject.toml` the following stuff:
```toml
[manage_django_project]
module_name="your_project_example"

# Django settings used for all commands except test/coverage/nox:
local_settings='your_project.settings.local'

# Django settings used for test/coverage/nox commands:
test_settings='your_project.settings.tests'
```

The `config` argument was remove from `execute_django_from_command_line()`, so your `__main__.py` must look like:

```python
from manage_django_project.manage import execute_django_from_command_line


def main():
    execute_django_from_command_line()


if __name__ == '__main__':
    main()
```


## Make new release

We use [cli-base-utilities](https://github.com/jedie/cli-base-utilities#generate-project-history-base-on-git-commitstags) to generate the history in this README.


To make a new release, do this:

* Increase your project version number
* Run tests to update the README
* commit the changes
* Create release


## history

[comment]: <> (✂✂✂ auto generated history start ✂✂✂)

* [v0.11.2](https://github.com/jedie/manage_django_project/compare/v0.11.1...v0.11.2)
  * 2026-01-30 - Update CI config
  * 2026-01-30 - Bugfix tests around "pip-audit"
  * 2026-01-30 - Update requirements and apply manageprojects updates
  * 2025-11-28 - Update README.md
  * 2025-11-28 - Add logo
  * 2025-11-28 - Update tests and run configs
  * 2025-11-28 - Update requirements
* [v0.11.1](https://github.com/jedie/manage_django_project/compare/v0.11.0...v0.11.1)
  * 2025-10-16 - Expand test matrix with Python v3.14
  * 2025-10-16 - Update requirements
* [v0.11.0](https://github.com/jedie/manage_django_project/compare/v0.10.1...v0.11.0)
  * 2025-09-21 - New manage command: "make_messages"
* [v0.10.1](https://github.com/jedie/manage_django_project/compare/v0.10.0...v0.10.1)
  * 2025-09-21 - fix code style
  * 2025-09-21 - Update django-tools
  * 2025-09-21 - Apply manageprojects updates
  * 2025-09-21 - Update requirements

<details><summary>Expand older history entries ...</summary>

* [v0.10.0](https://github.com/jedie/manage_django_project/compare/v0.9.3...v0.10.0)
  * 2025-09-03 - print always a new line before help text panel
  * 2025-09-03 - Replace Darker with Ruff
* [v0.9.3](https://github.com/jedie/manage_django_project/compare/v0.9.2...v0.9.3)
  * 2025-08-05 - Update text matrix: DJANGO_VERSIONS = ['5.2', '5.1', '4.2']
  * 2025-08-05 - Update requirements
  * 2025-07-29 - Add CallManagePy test helper (#68)
  * 2025-07-29 - Add CallManagePy test helper
* [v0.9.2](https://github.com/jedie/manage_django_project/compare/v0.9.1...v0.9.2)
  * 2025-06-02 - Run "pre-commit autoupdate" only if "pre-commit" is installed
* [v0.9.1](https://github.com/jedie/manage_django_project/compare/v0.9.0...v0.9.1)
  * 2025-04-30 - replace setuptools with hatchling
  * 2025-04-30 - modernize config.py
  * 2025-04-30 - Apply manageprojects updates
  * 2025-04-30 - Update requirements
* [v0.9.0](https://github.com/jedie/manage_django_project/compare/v0.8.0...v0.9.0)
  * 2025-02-12 - install pre commit in bootstrap
  * 2025-02-12 - Bugfix "publish" command
  * 2025-02-12 - Cleanup: Remove obsolete tox stuff
  * 2025-02-12 - pip-tools -> uv and tox -> nox
* [v0.8.0](https://github.com/jedie/manage_django_project/compare/v0.7.2...v0.8.0)
  * 2024-08-02 - Replace "safety" by "pip-audit" and add tooling for it.
  * 2024-08-02 - Update project setup
  * 2024-08-02 - Update requirements and add git pre commit hooks
  * 2024-05-21 - Update requirements
  * 2024-05-21 - Safety: Ignore CVE-2018-20225
  * 2024-05-21 - update from manageprojects template
* [v0.7.2](https://github.com/jedie/manage_django_project/compare/v0.7.1...v0.7.2)
  * 2024-02-20 - Add '--strip-extras' to pip-compile and update requirements
* [v0.7.1](https://github.com/jedie/manage_django_project/compare/v0.7.0...v0.7.1)
  * 2024-01-18 - Use typeguard in tests
  * 2024-01-18 - update requirements
  * 2024-01-18 - manageprojects updates + set min. Python to 3.9
* [v0.7.0](https://github.com/jedie/manage_django_project/compare/v0.6.4...v0.7.0)
  * 2023-12-19 - Apply manageprojects: Expand test matrix + update req. + skip Python 3.9
  * 2023-12-19 - Setup django for unittests
  * 2023-12-16 - Bugfix code style
  * 2023-12-16 - Use update_readme_history & as git hook
  * 2023-11-07 - Update requirements
* [v0.6.4](https://github.com/jedie/manage_django_project/compare/v0.6.3...v0.6.4)
  * 2023-11-01 - update requirements
* [v0.6.3](https://github.com/jedie/manage_django_project/compare/v0.6.2...v0.6.3)
  * 2023-11-01 - Update requirements
  * 2023-11-01 - Autogenerate history in README
  * 2023-11-01 - Bugfix subprocess timeout running manage commands
* [v0.6.2](https://github.com/jedie/manage_django_project/compare/v0.6.1...v0.6.2)
  * 2023-09-24 - Use tools from https://github.com/jedie/cli-base-utilities
* [v0.6.1](https://github.com/jedie/manage_django_project/compare/v0.6.0...v0.6.1)
  * 2023-09-24 - Erase coverage data always after test run
  * 2023-09-24 - Add manage command to interact with Playwright CLI
* [v0.6.0](https://github.com/jedie/manage_django_project/compare/v0.5.2...v0.6.0)
  * 2023-09-24 - Remove outdated history from README
  * 2023-09-24 - Nicer call command info
  * 2023-09-24 - NEW command: update_test_snapshot_files
  * 2023-09-24 - Auto erase coverage data
  * 2023-09-24 - Update requirements
* [v0.5.2](https://github.com/jedie/manage_django_project/compare/v0.5.1...v0.5.2)
  * 2023-08-17 - Bugfix: manageprojects must be a normal dependencies
* [v0.5.1](https://github.com/jedie/manage_django_project/compare/v0.5.0...v0.5.1)
  * 2023-08-17 - Use print_version from cli_base
  * 2023-08-17 - Update requirements
  * 2023-08-17 - cookiecutter_directory = "managed-django-project"
  * 2023-08-17 - apply template updates
* [v0.5.0](https://github.com/jedie/manage_django_project/compare/v0.4.1...v0.5.0)
  * 2023-08-15 - Use https://github.com/jedie/cli-base-utilities
  * 2023-08-04 - Update requirements
* [v0.4.1](https://github.com/jedie/manage_django_project/compare/v0.4.0...v0.4.1)
  * 2023-04-08 - Use get_pyproject_toml from manageprojects and add summarize output to update_req
* [v0.4.0](https://github.com/jedie/manage_django_project/compare/v0.3.0...v0.4.0)
  * 2023-04-07 - tests against different Django versions
  * 2023-04-07 - Enhance "update_req" command
* [v0.3.0](https://github.com/jedie/manage_django_project/compare/v0.2.2...v0.3.0)
  * 2023-04-05 - Move from `__main__.py` into `pyproject.toml`
  * 2023-04-05 - Bugfix tox run
  * 2023-04-05 - Update manage.py
  * 2023-04-05 - Delete README.md
  * 2023-04-05 - Small project updates
* [v0.2.2](https://github.com/jedie/manage_django_project/compare/v0.2.1...v0.2.2)
  * 2023-04-02 - fix code style
  * 2023-04-02 - apply manage projects update
  * 2023-04-02 - Ignore non `django.core.management.base.BaseCommand` based commands
  * 2023-04-02 - Update requirements
* [v0.2.1](https://github.com/jedie/manage_django_project/compare/v0.2.0...v0.2.1)
  * 2023-03-16 - fix test
  * 2023-03-16 - Add "Included Django management commands" to README
  * 2023-03-16 - typo
  * 2023-03-16 - Set v0.2.1
  * 2023-03-16 - Enhance docs
  * 2023-03-16 - Remove `prod_settings` and add `local_settings_commands` to `ManageConfig`
  * 2023-03-16 - Add test for bootstrap manage.py calls
  * 2023-03-16 - fix coverage by activating --concurrency=multiprocessing
  * 2023-03-15 - fix CI
  * 2023-03-15 - "tox" command: exit "normal" on failed run
  * 2023-03-15 - Add tests for "safety" command
  * 2023-03-15 - Test "tox" command
  * 2023-03-15 - Add test for "run_dev_server" command
  * 2023-03-15 - test "project_info" command
  * 2023-03-15 - Test command "install"
  * 2023-03-15 - Test command "code_sytle"
  * 2023-03-15 - Code cleanup: Remove unused files
  * 2023-03-14 - +Test coverage
  * 2023-03-14 - Test "update_req"
  * 2023-03-14 - Add basic test for "update_req"
  * 2023-03-14 - Add DocTest to unittests
  * 2023-03-14 - Add test for shell
  * 2023-03-14 - Skip broken commands
  * 2023-03-14 - remove debug print
* [v0.2.0](https://github.com/jedie/manage_django_project/compare/v0.1.1...v0.2.0)
  * 2023-03-13 - NEW: "./manage.py shell" cmd2 shell with all registered Django manage commands
* [v0.1.1](https://github.com/jedie/manage_django_project/compare/v0.1.0...v0.1.1)
  * 2023-03-13 - Use `distribution_name` in publish call
* [v0.1.0](https://github.com/jedie/manage_django_project/compare/v0.0.1...v0.1.0)
  * 2023-03-12 - Remove a existing '.coverage' before create a new one
  * 2023-03-12 - check settings
  * 2023-03-12 - Rename test settings and check the used settings in test
  * 2023-03-12 - Run tests with test settings, before publishing
  * 2023-03-12 - Update README.md
* [v0.0.1](https://github.com/jedie/manage_django_project/compare/99601ed...v0.0.1)
  * 2023-03-11 - init
  * 2023-03-11 - Initial commit

</details>


[comment]: <> (✂✂✂ auto generated history end ✂✂✂)
