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
        if self.pk is None:
            # newly created model, set the generation index automatically
            if self.index is None:
                generations = Generation.objects.filter(app_name=self.app_name).order_by('-index')
                if generations.exists():
                    self.index = generations[0].index + 1
                else:
                    self.index = 1