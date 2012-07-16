"""genia/models.py

Test cases for django-genia
"""

from django.test import TestCase
from django.db import models

from genia.models import Generation, GenerationalModelMixin


# these are models that will use genia
class Person(GenerationalModelMixin, models.Model):
    """Simple model to exercise the tests below"""
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class GenerationTest(TestCase):
    """Tests related to generations themselves"""
    def test_auto_index(self):
        """Check that each generation gets a new index"""
        gen1 = Generation.objects.create(app_name='test')
        gen2 = Generation.objects.create(app_name='test')
        gen3 = Generation.objects.create(app_name='test2')
        self.assertEquals(gen1.index, 1)
        self.assertEquals(gen2.index, 2)
        self.assertEquals(gen3.index, 1)

    def test_make_active(self):
        """Test make_active in the trivial case

        No other generations to contend with
        """
        gen1 = Generation.objects.create(app_name='test')
        gen1.make_active()
        self.assertTrue(gen1.active)

    def test_make_active_second(self):
        """Test make_active in the non-trivial case

        Here there are other generations to contend with
        """
        gen1 = Generation.objects.create(app_name='test')
        gen1.make_active()
        assert gen1.active   # precondition, already tested above
        gen2 = Generation.objects.create(app_name='test')
        gen2.make_active()
        gen1 = Generation.objects.get(pk=gen1.pk)   # refresh from DB
        self.assertTrue(gen2.active)
        self.assertFalse(gen1.active)

    # manager tests
    def test_manager_active(self):
        """Test the manager active method

        Should return only the active generation
        """
        _gen1 = Generation.objects.create(app_name='test')
        gen2 = Generation.objects.create(app_name='test')
        gen2.make_active()
        self.assertEqual(Generation.objects.active(app_name='test').pk, gen2.pk)


class GenerationalModelTest(TestCase):
    """Tests related to generational data models"""
    def setUp(self):
        self.gen1 = Generation.objects.create(app_name='genia')
        self.gen2 = Generation.objects.create(app_name='genia')
        self.gen2.make_active()

    def test_get_query_set(self):
        """Test default manager

        objects should return only the data in the active generation
        """
        Person.objects.create(name='Joe', generation=self.gen1)
        Person.objects.create(name='Bob', generation=self.gen2)
        self.assertQuerysetEqual(Person.objects.all(), ['<Person: Bob>'])

    def test_active_generation(self):
        """Test generational data class method active_generation"""
        self.assertEqual(Person.active_generation().pk, self.gen2.pk)