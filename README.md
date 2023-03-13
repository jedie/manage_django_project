# manage_django_project

[![tests](https://github.com/jedie/manage_django_project/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/jedie/manage_django_project/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/manage_django_project/branch/main/graph/badge.svg)](https://app.codecov.io/github/jedie/manage_django_project)
[![manage_django_project @ PyPi](https://img.shields.io/pypi/v/manage_django_project?label=manage_django_project%20%40%20PyPi)](https://pypi.org/project/manage_django_project/)
[![Python Versions](https://img.shields.io/pypi/pyversions/manage_django_project)](https://github.com/jedie/manage_django_project/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/manage_django_project)](https://github.com/jedie/manage_django_project/blob/main/LICENSE)

Helper to develop Django projects.


## How to use it

TBD


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

# start local dev. web server:
~/django-for-runners$ ./manage.py run_dev_server

# run tests:
~/django-for-runners$ ./manage.py test
# or with coverage
~/django-for-runners$ ./manage.py coverage
# or via tox:
~/django-for-runners$ ./manage.py tox
```


## history

* [**dev**](https://github.com/jedie/manage_django_project/compare/v0.1.1...main)
  * TBC
* [v0.1.1 - 13.03.2023](https://github.com/jedie/manage_django_project/compare/v0.1.0...v0.1.1)
  * Add `ProjectInfo.distribution_name` and set if from `pyproject.toml`
  * Use `distribution_name` in publish call
* [v0.1.0 - 12.03.2023](https://github.com/jedie/manage_django_project/compare/v0.0.1...v0.1.0)
  * publish command: Bugfix test run before publishing: use the "test" settings
  * coverage command: Remove a existing `.coverage` before create a new one
* v0.0.1 - 12.03.2023
  * Init first version
