=========
Plone CTL
=========

**A Plone CTL for running Plone sites**

*The Plone CTL is meant for run Plone in development and in production.*


Installation
============

We install plonectl in the global user site-packages, so that we can use it in multible projects.

.. code-block:: console

    $ pip install plonectl --user
    $ plonectl -l

To upgrade plonectl just do:

.. code-block:: console

    $ pip install -U plonectl --user
    Note: Make sure that the install directory is in $PATH ( e.g. export PATH=$PATH:$HOME/.local/bin/  )

If would like to use plonectl with pipenv, you can do it as follow:

.. code-block:: console

    $ mkdir cli
    $ cd cli
    $ pipenv install plonectl
    $ pipenv shell
    $ plonectl -l


Bash Auto Completion
--------------------

To enable auto completion plonectl provides the plonectl_autocomplete.sh script, put the following bash command into your bashrc:

If you installed plonectl in user global packages:

.. code-block:: console

    $ . ~/.local/bin/plonectl_autocomplete.sh


If you installed plonectl in a virtualenv it's:

.. code-block:: console

    $ . /path/to/your/virtualenv/bin/plonectl_autocomplete.sh


If you used pipenv to install plonectl, you have to find out the path to the virtualenv before:

.. code-block:: console

    $ pipenv --virtualenv
    /home/maik/.local/share/virtualenvs/pe-WnXOnVWH
    . /home/maik/.local/share/virtualenvs/pe-WnXOnVWH/bin/plonectl_autocomplete.sh


Usage
=====

Available Commands
------------------

.. code-block:: console

    $ plonectl --help
    Usage: plonectl [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

      Plone Command Line Interface (CLI)

    Options:
      -l, --list-templates
      -V, --versions
      -h, --help            Show this message and exit.

    Commands:
      instance
      zeoserver
      zeopack


Developer Guide
===============

Setup Developer Environment
---------------------------

.. code-block:: console

    $ git clone https://github.com/plone/plonectl/
    $ cd plonectl
    $ virtualenv .
    $ source bin/activate
    $ pip install -r requirements.txt
    $ python setup.py develop
    $ plonectl --help


.. Running Tests
.. -------------

.. You can run the tests using the following command:

.. .. code-block:: console

..     $ tox

.. or by installing py.test and run the test directly without tox:

.. .. code-block:: console

..     $ py.test test/

.. or a single test:

.. .. code-block:: console

..     $ py.test test/ -k test_get_package_root


Contribute
==========

- Issue Tracker: https://github.com/datakurre/plonectl/issues
- Source Code: https://github.com/datakurre/plonectl


License
=======

This project is licensed under the BSD license.
