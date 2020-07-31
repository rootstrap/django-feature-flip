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
        FeatureFactory(name='my_enabled_feature')
        actor = self._actor(1)

        self.assertFalse(self.feature_flip.enabled('my_enabled_feature', actor))

    def test_enabled_for_totally_enabled_feature(self):
        FeatureFactory(name='my_disabled_feature', totally_enabled=True)
        actor = self._actor(1)

        self.assertTrue(self.feature_flip.enabled('my_disabled_feature', actor))

    def test_enabled_for_non_existent_feature(self):
        actor = self._actor(1)
        try:
            self.feature_flip.enabled('non_existent_feature', actor)
        except FeatureFlip.FeatureFlipError as error:
            self.assertEqual(error.message, 'Feature non_existent_feature does not exist')

    def test_group_registration(self):
        FeatureFactory(name='my_feature', totally_enabled=False)
        FeatureFactory(name='my_other_feature', totally_enabled=True)

        # we register a group of all actors with flip_id() > 5
        self.feature_flip.register('flip_id_gt_5', lambda obj: obj.flip_id() > 5)

        # we register a group of all actors with flip_id() <= 5
        self.feature_flip.register('flip_id_lte_5', lambda obj: obj.flip_id() <= 5)

        disabled_actor = self._actor(1)
        enabled_actor = self._actor(6)

        self.feature_flip.activate_group('my_feature', 'flip_id_gt_5')
        self.feature_flip.activate_group('my_other_feature', 'flip_id_lte_5')

        self.assertTrue(FeatureFlip().enabled('my_feature', enabled_actor))
        self.assertFalse(FeatureFlip().enabled('my_feature', disabled_actor))

    def test_activate_group_for_non_existent_feature(self):
        self.feature_flip.register('my_group', lambda obj: obj.flip_id() > 5)

        try:
            self.feature_flip.activate_group('non_existent_feature', 'my_group')
        except FeatureFlip.FeatureFlipError as error:
            self.assertEqual(error.message, 'Feature non_existent_feature does not exist')

    def test_activate_group_for_non_existent_group(self):
        FeatureFactory(name='my_feature')

        try:
            self.feature_flip.activate_group('my_feature', 'non_existent_group')
        except FeatureFlip.FeatureFlipError as error:
            self.assertEqual(error.message, 'Group non_existent_group does not exist')
