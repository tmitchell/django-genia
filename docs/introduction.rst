============
Introduction
============

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

Why not just import everything in one big transaction?
------------------------------------------------------

Good question!  For `our <http://exoanalytic.com>`_ purposes, we need to commit transactions as we go for a number
of reasons.  The biggest is that we like to import data in parallel when possible and some of the tables we
reference are shared.  If you don't commit as you go, you're more likely to encounter ``IntegrityError`` and its ilk.