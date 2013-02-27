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
import optparse
from django.conf import settings

__author__ = 'Ben Welsh'
__credits__ = ['Ben Welsh', 'Lukasz Dziedzia', 'Shane Allgeier']
__maintainer__ = 'Shane Allgeier'
__version__ = '0.1.1'
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
        # Set the version of the test suite
        self._setup()

    def _setup(self):
        """
        Figure out which version of Django's test suite we have to play with.
        """
        from django import VERSION
        if VERSION[0] == 1 and VERSION[1] >= 2:
            self.run_tests = self._new_tests
        else:
            self.run_tests = self._old_tests

    def _old_tests(self, verbosity=1, interactive=False, extra_tests=[], **kwargs):
        """
        Fire up the Django test suite from before version 1.2
        """
        settings.configure(DEBUG=True, DATABASE_ENGINE='sqlite3', INSTALLED_APPS=self.INSTALLED_APPS + self.apps, ROOT_URLCONF=__name__)
        self._setup_urlpatterns()
        from django.test.simple import run_tests
        return run_tests(self.apps, verbosity=verbosity, interactive=interactive, extra_tests=extra_tests)

    def _new_tests(self, verbosity=1, interactive=False, extra_tests=None, failfast=False, **kwargs):
        """
        Fire up the Django test suite developed for version 1.2
        """
        settings.configure(
            DEBUG=True,
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                }
            },
            INSTALLED_APPS=self.INSTALLED_APPS + self.apps,
            ROOT_URLCONF=__name__,
        )
        self._setup_urlpatterns()
        from django.test.simple import DjangoTestSuiteRunner
        return DjangoTestSuiteRunner(verbosity=verbosity, interactive=interactive, failfast=failfast).run_tests(self.apps)

    def _setup_urlpatterns(self):
        try:
            from django.conf.urls import patterns, include, url
        except ImportError:
            from django.conf.urls.defaults import patterns, include, url
        urls = []
        for appname in self.apps:
            try:
                urls.append(('^%s/' % appname, include('%s.urls' % appname)))
            except ImportError:
                pass
        global urlpatterns
        urlpatterns = patterns('', *urls)


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
    failures = DjangoAppTest(*args.apps).run_tests(interactive=False, failfast=False)
    if failures:
        sys.exit(failures)

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(1)
