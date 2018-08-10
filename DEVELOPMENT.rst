===========================================
Lovely Webservices Status Development Notes
===========================================

Development Setup
=================

In order to setup the development sandbox you need the following:

 - Java 8+ installed to run the bootstrapping

 - Python 3.6+ installed and executable called `python3`

In order to setup your python environment run the following::

    ./gradlew dev

This will create a python virtualenv in the ``v`` directory with all
requirements installed.

Run Tests
=========

Use the gradle which also does any bootstrapping::

    ./gradlew test

Tests can also be run by calling pytest directly::

    ./v/bin/pytest tests

The `README.rst <README.rst>`_ file can be tested too::

    ./v/bin/pytest README.rst

Releases and Packages
=====================

Tagging
-------

Before creating a new distribution, a new version and tag should be created:

- Update the ``CHANGES.rst`` file and create the top paragraph for your version
- Commit your changes with a message like "prepare release x.y.z"
- Push to origin
- Create a tag by running ``./gradlew createTag``

Create source distribution
--------------------------

To build a source distribution run::

    ./gradlew sdist

Upload to PyPI
--------------

To upload the current tagged release to PyPI run::

    ./gradlew upload

Note this will only work if on a non dev version.
