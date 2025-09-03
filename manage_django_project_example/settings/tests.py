# ruff: noqa: F405

"""
    Django settings for running tests
"""

from .base import *  # noqa


ALLOWED_HOSTS = ['testserver']


# _____________________________________________________________________________
# Manage Django Project

INSTALLED_APPS.append('manage_django_project.apps.ManageDjangoProjectConfig')
