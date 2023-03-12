# manage_django_project

[![tests](https://github.com/jedie/manage_django_project/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/jedie/manage_django_project/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/manage_django_project/branch/main/graph/badge.svg)](https://app.codecov.io/github/jedie/manage_django_project)
[![manage_django_project @ PyPi](https://img.shields.io/pypi/v/manage_django_project?label=manage_django_project%20%40%20PyPi)](https://pypi.org/project/manage_django_project/)
[![Python Versions](https://img.shields.io/pypi/pyversions/manage_django_project)](https://github.com/jedie/manage_django_project/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/manage_django_project)](https://github.com/jedie/manage_django_project/blob/main/LICENSE)

Helper to develop Django projects.

## Start hacking

Just clone the project and start `./manage.py` to bootstrap a virtual environment:

```
# Install base requirements for bootstraping:
~$ sudo apt install python3-pip python3-venv

# Get the sources:
~$ git clone https://github.com/jedie/manage_django_project.git
~$ cd manage_django_project/

# Just call manage.py:
~/manage_django_project$ ./manage.py --help
...
[manage_django_project]
    code_style
    coverage
    install
    project_info
    run_dev_server
    safety
    tox
    update_req
...
```

## history


* [**dev**](https://github.com/jedie/manage_django_project/compare/v0.0.1...main)
  * TBC
* v0.0.1rc1 - 12.03.2023
  * Just create a pre-alpha release to save the PyPi package name ;)
