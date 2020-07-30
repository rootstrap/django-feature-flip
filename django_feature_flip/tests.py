from django.test import TestCase
from django.db import DataError, IntegrityError
from django_feature_flip.factories import FeatureFactory
from django_feature_flip.helpers import FeatureFlip
from unittest.mock import Mock


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


class FeatureFlipTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.feature_flip = FeatureFlip()

    def _actor(self, flip_id):
        actor = Mock()
        actor.flip_id.return_value = flip_id
        return actor

    def test_singleton(self):
        self.assertEqual(id(self.feature_flip), id(self.feature_flip))

    def test_enabled_for_not_totally_enabled_feature(self):
        FeatureFactory(name='my_feature', totally_enabled=False)
        actor = self._actor(1)

        self.assertFalse(self.feature_flip.enabled('my_feature', actor))

    def test_enabled_for_totally_enabled_feature(self):
        FeatureFactory(name='my_feature', totally_enabled=True)
        actor = self._actor(1)

        self.assertTrue(self.feature_flip.enabled('my_feature', actor))
