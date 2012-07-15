from django.test import TestCase
from django.db import models

from genia.models import Generation


# these are models that will use genia
class Person(models.Model):
    name = models.CharField(max_length=100)
    generation = models.ForeignKey(Generation)


class GenerationTest(TestCase):
    def test_auto_index(self):
        """Check that each subsequent generation within an app created gets a new index"""
        g1 = Generation.objects.create(app_name='test')
        g2 = Generation.objects.create(app_name='test')
        g3 = Generation.objects.create(app_name='test2')
        self.assertEquals(g1.index, 1)
        self.assertEquals(g2.index, 2)
        self.assertEquals(g3.index, 1)

    def test_make_current(self):
        g1 = Generation.objects.create(app_name='test')
        g1.make_current()
        self.assertTrue(g1.current)

    def test_make_current_second(self):
        g1 = Generation.objects.create(app_name='test')
        g1.make_current()
        assert g1.current   # precondition, already tested above
        g2 = Generation.objects.create(app_name='test')
        g2.make_current()
        g1 = Generation.objects.get(pk=g1.pk)   # refresh from DB
        self.assertTrue(g2.current)
        self.assertFalse(g1.current)