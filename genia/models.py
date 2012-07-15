from django.db import models
from utils import get_app_name_for_model


class GenerationManager(models.Manager):
    def active(self, app_name):
        return self.get(active=True, app_name=app_name)


class Generation(models.Model):
    app_name = models.CharField(max_length=255)
    index = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(null=True)
    active = models.BooleanField()
    objects = GenerationManager()
    class Meta:
        unique_together = ('app_name', 'index')

    def save(self, *args, **kwargs):
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
        if self.active:
            return
        active_qs = Generation.objects.filter(app_name=self.app_name).filter(active=True)
        if active_qs.exists():
            active_qs.update(active=False)
        self.active = True
        self.save()

    def __unicode__(self):
        return u"%s #%d" % (self.app_name, self.index)


class GenerationalModelManager(models.Manager):
    def get_query_set(self):
        qset = super(GenerationalModelManager, self).get_query_set()
        if qset.exists():
            app_name = get_app_name_for_model(self.model)
            qset = qset.filter(generation=Generation.objects.get(app_name=app_name, active=True))
        return qset


class GenerationalModelMixin(models.Model):
    generation = models.ForeignKey(Generation)
    objects = GenerationalModelManager()
    class Meta:
        abstract = True

    @classmethod
    def active_generation(cls):
        return Generation.objects.active(app_name=get_app_name_for_model(cls))