from django.db import models


class Generation(models.Model):
    app_name = models.CharField(max_length=255)
    index = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(null=True)
    current = models.BooleanField()
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

    def make_current(self):
        if self.current:
            return
        current_qset = Generation.objects.filter(app_name=self.app_name).filter(current=True)
        if current_qset.exists():
            current_qset.update(current=False)
        self.current = True
        self.save()