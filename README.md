# manage_django_project

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
* `project_info` - Information about the current Django project
* `publish` - Build a new release and publish it to PyPi
* `run_dev_server` - Setup test project and run django developer server
* `safety` - Run safety check against current requirements files
* `shell` - Go into cmd2 shell with all registered Django manage commands
* `tox` - Run tests via tox
* `update_req` - Update project requirements via pip-tools

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

# Django settings used for all commands except test/coverage/tox:
local_settings='your_project.settings.local'

# Django settings used for test/coverage/tox commands:
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
# or via tox:
~/django-for-runners$ ./manage.py tox
```


## Backwards-incompatible changes

### v0.2.x -> v0.3.x

The config was moved out from `__main__.py` into `pyproject.toml`

You must add in your `pyproject.toml` the following stuff:
```toml
[manage_django_project]
module_name="your_project_example"

# Django settings used for all commands except test/coverage/tox:
local_settings='your_project.settings.local'

# Django settings used for test/coverage/tox commands:
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


## history

* [**dev**](https://github.com/jedie/manage_django_project/compare/v0.3.0...main)
  * TBC
* [v0.3.0 - 05.04.2023](https://github.com/jedie/manage_django_project/compare/v0.2.2...v0.3.0)
  * Refactor config: Move from `__main__.py` into `pyproject.toml` see backwards-incompatible changes
  * Small project changes + requirements update
* [v0.2.2 - 02.04.2023](https://github.com/jedie/manage_django_project/compare/v0.2.1...v0.2.2)
  * Ignore non `django.core.management.base.BaseCommand` based commands.
* [v0.2.1 - 16.03.2023](https://github.com/jedie/manage_django_project/compare/v0.2.0...v0.2.1)
  * Add more tests
  * Enhance README
  * Code cleanup
* [v0.2.0 - 14.03.2023](https://github.com/jedie/manage_django_project/compare/v0.1.1...v0.2.0)
  * Add a optional shell via cmd2
* [v0.1.1 - 13.03.2023](https://github.com/jedie/manage_django_project/compare/v0.1.0...v0.1.1)
  * Add `ProjectInfo.distribution_name` and set if from `pyproject.toml`
  * publish command: Use `distribution_name` in publish call
  * publish command: Display used settings for `publish_package()`
* [v0.1.0 - 12.03.2023](https://github.com/jedie/manage_django_project/compare/v0.0.1...v0.1.0)
  * publish command: Bugfix test run before publishing: use the "test" settings
  * coverage command: Remove a existing `.coverage` before create a new one
* v0.0.1 - 12.03.2023
  * Init first version
