from django.db import models


class Feature(models.Model):
    name = models.CharField(max_length=40, unique=True)
    totally_enabled = models.BooleanField(default=False)

    def enabled(self, actor):
        return self.totally_enabled

    def __str__(self):
        return self.name
