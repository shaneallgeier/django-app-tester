django-app-tester
=================

About
-----
django_apptest is a command-line utility for testing your pluggable Django apps
outside of a fully-configured project. It will bootstrap Django and run the tests
inside your app without having to create a Django project, fill out a settings.py
file or any other preparation.


Usage
-----
To run the test suite on an app called **my_app**, ``cd`` into the directory above
the my_app directory and run::

    $ django_apptest my_app

    
Use as a module
---------------

The simplest way of using django_apptest as a module is via the ``DjangoAppTest``
class.

.. code-block:: python

    >>> from django_apptest import DjangoAppTest
    >>> DjangoAppTest('my_app', 'your_app').run_tests()