.. django-genia documentation master file, created by
   sphinx-quickstart on Sun Jul 15 14:06:26 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-genia's documentation!
========================================

django-genia is a relatively simple set of models and helpers for handling generational data.

What is generational data?
--------------------------

Generational data refers to data within a Django app that is relevant together at a given point in time.  We may create
different records at different times, but we only want to display the records that go together.  Each of these snapshots
we call a `generation`.

Introduction
------------

Sometimes you have data that takes a long time to create/import but that only makes sense when loaded completely.  While
the data is loading you may not want your users to see it.  This app allows you to put each data import into its own
generation, and make the generation active at the end.  By default, queries against your generational models will only
return records in the active generation.

"But wait," you say, "why don't you just import everything in a single transaction and commit it when you're done?"

Good question!  For `our <http://exoanalytic.com>`_ purposes, we need to commit transactions as we go for a number
of reasons.  The biggest is that we like to import data in parallel when possible and some of the tables we
reference are shared.  If you don't commit as you go, you're more likely to encounter `IntegrityError` and such.

Contributing
------------

This project is open source and licensed under the `BSD <http://opensource.org/licenses/BSD-3-Clause>`_ license.
It is hosted at `GitHub <http://github.com>`_ so head over to the `project page <https://github.com/tmitchell/django-genia>`_
if you want to report an issue, request a feature or contribute to its development.

Contents
--------

.. toctree::
   :maxdepth: 2

   usage
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

