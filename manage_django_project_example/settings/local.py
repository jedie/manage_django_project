# ruff: noqa: F405

"""
    Django settings for local development
"""

from .base import *  # noqa


# _____________________________________________________________________________
# Manage Django Project

INSTALLED_APPS.append('manage_django_project.apps.ManageDjangoProjectConfig')
