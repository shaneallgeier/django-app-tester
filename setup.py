#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup for django_apptest"""

from setuptools import setup


def version():
    """Return version string."""
    with open('django_apptest.py') as input_file:
        for line in input_file:
            if line.startswith('__version__'):
                import ast
                return ast.literal_eval(line.split('=')[1].strip())


with open('README.rst') as readme:
    setup(
        name='django-app-tester',
        version=version(),
        description='A tool that runs the Django test suite for a given application'
                    ' without requiring a fully-configured project',
        long_description=readme.read(),
        author='Shane Allgeier',
        author_email='shaneallgeier@gmail.com',
        url='https://github.com/shaneallgeier/django-app-tester',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Unix Shell',
        ],
        keywords='automation, unit tests, django app testing',
        py_modules=['django_apptest'],
        entry_points={'console_scripts': ['django_apptest = django_apptest:main', 'djapptest = django_apptest:main']},
    )
