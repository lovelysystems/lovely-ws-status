===========================================
Lovely Webservices Status Development Notes
===========================================

Development Setup
=================

In order to setup your python environment run the following::

    ./gradlew venv

This will create a python virtualenv in the ``v`` directory.


Dependencies
============

Adding new requirements requires the following steps:

- Add the dependency to the ``requires`` list in ``setup.py``
- To find out what are the latest versions of all dependencies make a dry run
  with pip-compile: ``./v/bin/pip-compile -n``
- Set the minimum (and maximum if necessary) versions in ``requirements.txt``.
  This is a library, so do not hard-pin any versions: Provide something like
  ``some_package>=1.0,<=2.0``.
- Update the ``requirements-test.txt``:
  ``./v/bin/pip-compile requirements-test.in``


Run Tests
=========

Initially prepare your PIP environment (or when dependencies are modified)::

    ./gradlew testenv

Tests are held in the ``tests`` directory. Running tests is done via the
pytest package with::

    ./v/bin/pytest tests

The `README.rst <README.rst>`_ file can be tested too::

    ./v/bin/pytest README.rst
