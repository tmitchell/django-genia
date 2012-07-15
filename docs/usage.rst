=====
Usage
=====

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

The easiest way to get started is to edit your Django app's ``models.py`` to use
:py:class:`genia.models.GenerationalModelMixin`:

.. code-block:: python
    :emphasize-lines: 2,4

    from django.db import models
    from genia.models import GenerationalModelMixin

    class Person(GenerationalModelMixin, models.Model):
        name = models.CharField(max_length=100)

        def __unicode__(self):
            return self.name

This mixin will add a ``generation`` field to your model which is a ``ForeignKey`` to a
:py:class:`genia.models.Generation`.  It also overrides your model's default manager to use
:py:class:`genia.models.GenerationalModelManager`.

If you need to customize this (e.g. your model already has its own custom manager), you can use the following template:

.. code-block:: python
    :emphasize-lines: 2,6,8

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

