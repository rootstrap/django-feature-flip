from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Group(models.Model):
    name = models.CharField(max_length=40, unique=True, db_index=True, null=False)

    def __str__(self):
        return self.name


class Feature(models.Model):
    name = models.CharField(max_length=40, unique=True, db_index=True, null=False)
    totally_enabled = models.BooleanField(default=False, null=False)
    time_percentage = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    groups = models.ManyToManyField(Group, related_name='features')

    def __str__(self):
        return self.name

    def group_names(self):
        return self.groups.all().values_list('name', flat=True)
