
"""Main helper file of FeatureFlip."""

from django_feature_flip.models import Group, Feature


class FeatureFlip:
    """Main class, singleton that should always be instanciated as FeatureFlip()."""

    class FeatureFlipError(Exception):
        """Default class for the FeatureFlip errors."""

        def __init__(self, message):
            """Initialize instance."""
            self.message = message

    class __FeatureFlip:
        """Initializer class for the singleton of FeatureFlip."""

        def __init__(self):
            """Initialize instance."""
            self.groups = {}

        def __str__(self):
            return repr(self)
    instance = None

    def __init__(self):
        """Initialize instance."""
        if not FeatureFlip.instance:
            FeatureFlip.instance = FeatureFlip.__FeatureFlip()

    def __getattr__(self, name):
        """Get attribute."""
        return getattr(self.instance, name)

    def enabled(self, feature_name, actor=None):
        """Check if a feature is enabled for an actor."""
        feature = get_feature_or_raise_error(feature_name)

        if feature.totally_enabled:
            return True
        elif actor:
            return self.feature_enabled_for_a_group_of_actor(feature, actor)
        else:
            return False

    def register(self, group_name, func):
        """Register the group of actors.

        The group is defined as every actor that returns true to func(actor).
        """
        Group.objects.get_or_create(name=group_name)

        self.groups[group_name] = func

    def activate_group(self, feature_name, group_name):
        """Turn on the group for a feature."""
        feature = get_feature_or_raise_error(feature_name)

        get_group_or_raise_error(group_name).features.add(feature)

    def feature_enabled_for_a_group_of_actor(self, feature, actor):
        """Check if a feature is enabled for a group of actors."""
        groups_names = [group.name for group in feature.group_set.all()]
        return any(self.groups[group_name](actor) for group_name in groups_names)


def get_feature_or_raise_error(feature_name):
    """Get the feature based on the name.

    Given a feature name, returns the correspondant feature or raises
    a FeatureFlip.FeatureFlipError error.
    """
    try:
        return Feature.objects.get(name=feature_name)
    except Feature.DoesNotExist:
        raise FeatureFlip.FeatureFlipError(f'Feature {feature_name} does not exist')


def get_group_or_raise_error(group_name):
    """Get the group based on the name.

    Given a group name, returns the correspondant feature or raises
    a FeatureFlip.FeatureFlipError error.
    """
    try:
        return Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        raise FeatureFlip.FeatureFlipError(f'Group {group_name} does not exist')
