from django.test import TestCase
from django.db import DataError, IntegrityError
from django_feature_flip.factories import FeatureFactory


class FeatureTestCase(TestCase):
    def test_uniqueness_of_name(self):
        FeatureFactory(name='repeated_name')

        with self.assertRaises(IntegrityError):
            FeatureFactory(name='repeated_name')

    def test_max_of_40_characters_of_name(self):
        with self.assertRaises(DataError):
            FeatureFactory(
                name='This is a very large name, '
                'features should have short names'
            )
