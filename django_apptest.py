#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A quick way to run the Django test suite without a fully-configured project.

Example usage:

    >>> DjangoAppTest('app1', 'app2')

Based on a script published by Lukasz Dziedzia at:
http://stackoverflow.com/a/3851333/1951234
"""

import os
import sys
import argparse
from django.conf import settings

__author__ = 'Ben Welsh'
__credits__ = ['Ben Welsh', 'Lukasz Dziedzia', 'Shane Allgeier']
__maintainer__ = 'Shane Allgeier'
__version__ = '0.1'
__license__ = 'Public Domain'


class DjangoAppTest(object):
    DIRNAME = os.path.dirname(__file__)
    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
    )

    def __init__(self, *args, **kwargs):
        self.apps = args
        # Get the version of the test suite
        self.version = self.get_test_version()
        # Call the appropriate one
        if self.version == 'new':
            self._new_tests()
        else:
            self._old_tests()

    def get_test_version(self):
        """
        Figure out which version of Django's test suite we have to play with.
        """
        from django import VERSION
        if VERSION[0] == 1 and VERSION[1] >= 2:
            return 'new'
        else:
            return 'old'

    def _old_tests(self):
        """
        Fire up the Django test suite from before version 1.2
        """
        settings.configure(DEBUG=True,
                           DATABASE_ENGINE='sqlite3',
                           DATABASE_NAME=os.path.join(
                           self.DIRNAME, 'database.db'),
                           INSTALLED_APPS=self.INSTALLED_APPS + self.apps
                           )
        from django.test.simple import run_tests
        failures = run_tests(self.apps, verbosity=1, interactive=False)
        if failures:
            sys.exit(failures)

    def _new_tests(self):
        """
        Fire up the Django test suite developed for version 1.2
        """
        settings.configure(
            DEBUG=True,
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': os.path.join(self.DIRNAME, 'database.db'),
                    'USER': '',
                    'PASSWORD': '',
                    'HOST': '',
                    'PORT': '',
                }
            },
            INSTALLED_APPS=self.INSTALLED_APPS + self.apps
        )
        from django.test.simple import DjangoTestSuiteRunner
        failures = DjangoTestSuiteRunner(verbosity=1, interactive=False,
                                         failfast=False).run_tests(self.apps)
        if failures:
            sys.exit(failures)


def main():
    """
    What do when the user hits this file from the shell.

    Example usage:

        $ djapptest app1 app2

    """
    parser = argparse.ArgumentParser(
        usage='[args]',
        description='Run Django tests on the provided applications.'
    )
    parser.add_argument('apps', nargs='+', type=str)
    args = parser.parse_args()
    sys.path.append(os.getcwd())
    DjangoAppTest(*args.apps)

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(1)
