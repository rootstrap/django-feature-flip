import factory

from django_feature_flip.models import Actor, Feature


FAKE = factory.faker.faker.Faker()


class FeatureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Feature

    name = factory.Faker('name')
    totally_enabled = False


class ActorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Actor

    flip_id = factory.Sequence(lambda n: n)
