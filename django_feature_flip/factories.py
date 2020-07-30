import factory

FAKE = factory.faker.faker.Faker()


class FeatureFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'django_feature_flip.Feature'

    name = factory.Faker('name')
