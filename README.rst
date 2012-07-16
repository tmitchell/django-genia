============
django-genia
============

Introduction
============

Genia is a simple pluggable Django app that helps manage generations of data

What is generational data?
--------------------------

Generational data refers to data within a Django app that is relevant together at a given point in time.  We may create
different records at different times, but we only want to display the records that go together.  Each of these snapshots
we call a `generation`.

Why would I want to use django-genia?
-------------------------------------

Sometimes you have data that takes a long time to create/import but that only makes sense when loaded completely.  While
the data is loading you may not want your users to see it.

django-genia makes it easy to support this workflow.

django-genia gives you simple hooks to put each data import into its own generation, and then make the generation
active at the end.  By default, queries against your generational models will only return records in the active generation.

Getting Started
===============

Prerequisites
-------------

* Django version 1.2 or greater (may work with earlier versions but untested)

Installation
------------

.. note:: We assume you're using pip+virtualenv+virtualenvwrapper.  If not, `start now <http://lmgtfy.com/?q=pip+virtualenv+virtualenvwrapper+tutorial>`_.

Install django-genia::

    $ pip install django-genia

Setup
-----

The easiest way to get started is to edit your Django app's ``models.py`` to use ``GenerationalModelMixin``:

    from django.db import models
    from genia.models import GenerationalModelMixin

    class Person(GenerationalModelMixin, models.Model):
        name = models.CharField(max_length=100)

        def __unicode__(self):
            return self.name

This mixin will add a ``generation`` field to your model which is a ``ForeignKey`` to a
``genia.models.Generation``.  It also overrides your model's default manager to use
``genia.models.GenerationalModelManager``.

If you need to customize this (e.g. your model already has its own custom manager), you can use the following template:

    from django.db import models
    from genia.models import Generation, GenerationalModelManager

    class Person(models.Model):
        name = models.CharField(max_length=100)
        generation = models.ForeignKey(Generation)
        objects = YourCustomManager()
        active_objects = GenerationalModelManager()

        def __unicode__(self):
            return self.name

If your model defines fields with ``unique=True``, they may not work as expected.  In this case, you should update
your model definition to use ``unique_together`` along with the ``generation`` field.

Usage
-----

The basic use case is if you have to import a lot of data at once into an app, but you don't want it to "go live" until
it's all done loading.  In this case, you would follow the following workflow:

#. Create a new generation
#. Start importing your data against this new generation
#. Once the import completes, set the new generation to be active

Here's an interactive session showing this workflow:

    >>> from genia.models import Generation
    >>> from my_app.loader import load_people
    >>> new_gen = Generation('my_app')
    >>> load_people(generation=new_gen)
    ...
    >>> new_gen.make_active()

Contributing
============

This project is open source and licensed under the `BSD <http://opensource.org/licenses/BSD-3-Clause>`_ license.
It is hosted at `GitHub <http://github.com>`_ so head over to the `project page <https://github.com/tmitchell/django-genia>`_
if you want to report an issue, request a feature or contribute to its development.