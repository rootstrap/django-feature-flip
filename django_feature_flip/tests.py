from django.test import TestCase
from django.db import DataError, IntegrityError
from django_feature_flip.factories import ActorFactory, FeatureFactory
from django_feature_flip.models import Actor
from django_feature_flip.helpers import FeatureFlip
from unittest.mock import Mock


class FeatureTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.feature = FeatureFactory()
        cls.actor_of_feature = ActorFactory()
        cls.feature.actors.add(cls.actor_of_feature)
        # other features
        cls.other_features = FeatureFactory.create_batch(size=10)
        cls.other_actor = ActorFactory()
        cls.other_actors = cls.other_features[0].actors.add(cls.other_actor)

    def test_uniqueness_of_name(self):
        FeatureFactory(name='repeated_name')

        with self.assertRaises(IntegrityError):
            FeatureFactory(name='repeated_name')

    def test_max_of_40_characters_of_name(self):
        with self.assertRaises(DataError):
            FeatureFactory(name='This is a very large name, features should have short names')

    def test_has_actor_when_actor_has_feature(self):
        self.assertTrue(self.feature.has_actor(self.actor_of_feature.flip_id))

    def test_has_actor_when_actor_does_not_have_feature(self):
        self.assertFalse(self.feature.has_actor(self.other_actor.flip_id))

    def test_has_actor_when_actor_does_not_exist(self):
        self.assertFalse(self.feature.has_actor(Actor.objects.last().id + 1))


class ActorTestCase(TestCase):
    def test_uniqueness_of_flip_id(self):
        ActorFactory(flip_id=12)

        with self.assertRaises(IntegrityError):
            ActorFactory(flip_id=12)


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

    def test_enabled_for_enabled_actor(self):
        feature = FeatureFactory()
        actor = ActorFactory(flip_id=1)
        feature.actors.add(actor)
        actor_object = self._actor(1)

        self.assertTrue(self.feature_flip.enabled(feature.name, actor_object))

    def test_enabled_for_disabled_actor(self):
        feature = FeatureFactory()
        actor = ActorFactory(flip_id=1)
        feature.actors.add(actor)
        actor_object = self._actor(2234)

        self.assertFalse(self.feature_flip.enabled(feature.name, actor_object))

    def test_enabled_for_non_existent_actor(self):
        feature = FeatureFactory()
        actor = ActorFactory(flip_id=1)
        feature.actors.add(actor)
        actor_object = self._actor(Actor.objects.last().id + 1)

        self.assertFalse(self.feature_flip.enabled(feature.name, actor_object))

    def test_enabled_for_invalid_actor(self):
        feature = FeatureFactory()
        actor_object = 12  # Does not implement flip_id()

        with self.assertRaises(AttributeError):
            self.feature_flip.enabled(feature.name, actor_object)

    def test_enable_actor_for_enabled_actor(self):
        feature = FeatureFactory()
        actor = ActorFactory(flip_id=1)
        feature.actors.add(actor)
        actor_object = self._actor(1)
        self.feature_flip.enable_actor(feature.name, actor_object)

        self.assertTrue(self.feature_flip.enabled(feature.name, actor_object))

    def test_enable_actor_for_non_enabled_actor(self):
        feature = FeatureFactory()
        ActorFactory(flip_id=1)
        actor_object = self._actor(1)
        self.feature_flip.enable_actor(feature.name, actor_object)

        self.assertTrue(self.feature_flip.enabled(feature.name, actor_object))

    def test_enable_actor_for_non_existent_actor(self):
        feature = FeatureFactory()
        actor_object = self._actor(1)

        self.assertFalse(self.feature_flip.enabled(feature.name, actor_object))

    def test_enable_actor_for_invalid_actor(self):
        feature = FeatureFactory()
        actor_object = 12  # Does not implement flip_id()

        with self.assertRaises(AttributeError):
            self.feature_flip.enable_actor(feature.name, actor_object)
