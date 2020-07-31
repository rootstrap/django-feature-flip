from django.db import models


class Feature(models.Model):
    name = models.CharField(max_length=40, unique=True)
    totally_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=40, unique=True, null=False)
    features = models.ManyToManyField(Feature)

    def __str__(self):
        return self.name
