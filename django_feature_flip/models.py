from django.db import models


class Actor(models.Model):
    flip_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.flip_id


class Feature(models.Model):
    name = models.CharField(max_length=40, unique=True)
    totally_enabled = models.BooleanField(default=False)
    actors = models.ManyToManyField(Actor, related_name='features')

    def __str__(self):
        return self.name

    def has_actor(self, flip_id):
        return self.actors.filter(flip_id=flip_id).exists()

    def add_actor(self, flip_id):
        actor, _ = Actor.objects.get_or_create(flip_id=flip_id)

        self.actors.add(actor)


class Group(models.Model):
    name = models.CharField(max_length=40, unique=True, null=False)
    features = models.ManyToManyField(Feature)

    def __str__(self):
        return self.name
