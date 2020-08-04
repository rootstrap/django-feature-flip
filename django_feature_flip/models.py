from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Feature(models.Model):
    name = models.CharField(max_length=40, unique=True)
    totally_enabled = models.BooleanField(default=False)
    time_percentage = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=40, unique=True, null=False)
    features = models.ManyToManyField(Feature)

    def __str__(self):
        return self.name
