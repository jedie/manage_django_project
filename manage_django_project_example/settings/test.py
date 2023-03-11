# flake8: noqa: E405

"""
    Django settings for running tests
"""

from .base import *  # noqa


# _____________________________________________________________________________
# Manage Django Project

INSTALLED_APPS.append('manage_django_project')
MANAGE_DJANGO_PROJECT_MODULE_NAME = 'manage_django_project_example'
