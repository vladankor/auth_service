from django.db import models
from django.utils import timezone


class MixModified(models.Model):
    modified_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(MixModified, self).save(*args, **kwargs)

    class Meta:
        abstract = True
