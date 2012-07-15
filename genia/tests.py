from django.test import TestCase
from django.db import models

from genia.models import Generation


# these are models that will use genia
class Person(models.Model):
    name = models.CharField(max_length=100)
    generation = models.ForeignKey(Generation)


class GenerationTest(TestCase):
    def test_auto_index(self):
        g1 = Generation.objects.create(app_name='test')
        g2 = Generation.objects.create(app_name='test')
        self.assertEquals(g1.index, 1)
        self.assertEquals(g2.index, 2)