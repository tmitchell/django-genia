from django.test import TestCase
from django.db import models

from genia.models import Generation, GenerationalModelMixin


# these are models that will use genia
class Person(GenerationalModelMixin, models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class GenerationTest(TestCase):
    def test_auto_index(self):
        """Check that each subsequent generation within an app created gets a new index"""
        g1 = Generation.objects.create(app_name='test')
        g2 = Generation.objects.create(app_name='test')
        g3 = Generation.objects.create(app_name='test2')
        self.assertEquals(g1.index, 1)
        self.assertEquals(g2.index, 2)
        self.assertEquals(g3.index, 1)

    def test_make_active(self):
        g1 = Generation.objects.create(app_name='test')
        g1.make_active()
        self.assertTrue(g1.active)

    def test_make_active_second(self):
        g1 = Generation.objects.create(app_name='test')
        g1.make_active()
        assert g1.active   # precondition, already tested above
        g2 = Generation.objects.create(app_name='test')
        g2.make_active()
        g1 = Generation.objects.get(pk=g1.pk)   # refresh from DB
        self.assertTrue(g2.active)
        self.assertFalse(g1.active)

    # manager tests
    def test_manager_active(self):
        g1 = Generation.objects.create(app_name='test')
        g2 = Generation.objects.create(app_name='test')
        g2.make_active()
        self.assertEqual(Generation.objects.active(app_name='test').pk, g2.pk)


class GenerationalModelTest(TestCase):
    def setUp(self):
        self.g1 = Generation.objects.create(app_name='genia')
        self.g2 = Generation.objects.create(app_name='genia')
        self.g2.make_active()

    def test_get_query_set(self):
        p1 = Person.objects.create(name='Joe', generation=self.g1)
        p2 = Person.objects.create(name='Bob', generation=self.g2)
        self.assertQuerysetEqual(Person.objects.all(), ['<Person: Bob>'])

    def test_active_generation(self):
        p1 = Person.objects.create(name='Joe', generation=self.g1)
        self.assertEqual(Person.active_generation().pk, self.g2.pk)