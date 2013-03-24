=========================
Using Piccolo from Jython
=========================

Piccolo2D.Java_  is a zoomable GUI framework built on top of Swing.
This repository contains copies of their introductory examples,
rewritten in Python syntax using Jython.

Instructions
============

To run these files, first `install Jython`_. Dependencies,
including Piccolo2D.Java_, are installed using jip_.
It is recommended to install jip_ into a ``virtualenv``,
as described on the `jip homepage`_.
Once `jip` is installed, you can either install this package with::

  jython setup.py install

or simply install the required jars with::

  jython setup.py resolve

and then run the example files with Jython; e.g.,::

  jython piccolo2d/examples/graph_editor.py

.. _Piccolo2D.Java: http://www.piccolo2d.org/
.. _install Jython: http://wiki.python.org/jython/InstallationInstructions
.. _jip: http://sunng87.github.com/jip/
.. _jip homepage: http://sunng87.github.com/jip/