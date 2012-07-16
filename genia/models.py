"""Django models, managers and mixins

For supporting generational data with django-genia
"""

from django.db import models
from django.utils.timezone import now

from genia.utils import get_app_name_for_model


class GenerationManager(models.Manager):
    """Manager for generation objects"""
    def active(self, app_name):
        """Get the one active generation for the given app

            :param app_name: Name of the app
            :type app_name: String
            :return: Active generation
            :rtype: Generation object
        """
        return self.get(active=True, app_name=app_name)


class Generation(models.Model):
    """Stores history of data generations for a given app"""
    app_name = models.CharField(max_length=255)
    index = models.IntegerField(help_text='Generation number for this app')
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(null=True,
        help_text='Timestamp of the last time the data was changed.  Manually set.')
    active = models.BooleanField(help_text='Is this the active generation for the given app? '
       'Note that only one generation can be active at a time')
    objects = GenerationManager()
    class Meta:
        unique_together = ('app_name', 'index')

    def save(self, *args, **kwargs):
        """Override base model save method

        Automatically sets the index of a new generation to the right (incremented) value.
        """
        app_generations = Generation.objects.filter(app_name=self.app_name)
        if self.pk is None:
            # newly created model, set the generation index automatically
            if self.index is None:
                generations = app_generations.order_by('-index')
                if generations.exists():
                    self.index = generations[0].index + 1
                else:
                    self.index = 1
        super(Generation, self).save(*args, **kwargs)

    def make_active(self):
        """Set the model to be the active generation for its app

        If there is already an active generation, it will be unset.
        """
        if self.active:
            return
        active_qs = Generation.objects.filter(app_name=self.app_name, active=True)
        if active_qs.exists():
            active_qs.update(active=False)
        self.active = True
        self.save()

    def ping(self):
        self.last_updated = now()
        self.save()

    def __unicode__(self):
        return u"%s #%d" % (self.app_name, self.index)


class GenerationalModelManager(models.Manager):
    """Manager for models that are implementing generational data"""
    def get_query_set(self):
        """Override the base get_query_set

            :return: Current QuerySet filtered to only objects in the active generation
            :rtype: QuerySet object
        """
        qset = super(GenerationalModelManager, self).get_query_set()
        if qset.exists():
            qset = qset.filter(generation=self.model.active_generation())
        return qset


class GenerationalModelMixin(models.Model):
    """Mixin class for models that represent generational data"""
    generation = models.ForeignKey(Generation)
    objects = GenerationalModelManager()
    class Meta:
        abstract = True

    @classmethod
    def active_generation(cls):
        """Get the active generation for this model's application data

            :return: Active generation for the model's app
            :rtype: Generation object
        """
        return Generation.objects.active(app_name=get_app_name_for_model(cls))