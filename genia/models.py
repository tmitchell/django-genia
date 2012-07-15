from django.db import models


class Generation(models.Model):
    app_name = models.CharField(max_length=255)
    index = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(null=True)
    current = models.BooleanField()
    class Meta:
        unique_together = ('app_name', 'index')