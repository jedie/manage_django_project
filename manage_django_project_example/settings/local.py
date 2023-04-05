# flake8: noqa: E405

"""
    Django settings for local development
"""

from .base import *  # noqa


# _____________________________________________________________________________
# Manage Django Project

INSTALLED_APPS.append('manage_django_project.apps.ManageDjangoProjectConfig')
