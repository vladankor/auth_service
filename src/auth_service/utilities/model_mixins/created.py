from django.db import models
from django.utils import timezone


class MixCreated(models.Model):
    created = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        super(MixCreated, self).save(*args, **kwargs)

    class Meta:
        abstract = True
