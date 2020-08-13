from django_feature_flip.models import Group, Feature


class FeatureFlip:
    class FeatureFlipError(Exception):
        def __init__(self, message):
            self.message = message

    class __FeatureFlip:
        def __init__(self):
            self.groups = {}

        def __str__(self):
            return repr(self)

    instance = None

    def __init__(self):
        if not FeatureFlip.instance:
            FeatureFlip.instance = FeatureFlip.__FeatureFlip()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def enabled(self, feature_name, actor=None):
        feature = get_feature_or_raise_error(feature_name)

        return feature.totally_enabled or self.feature_enabled_for_actor(feature, actor)

    def register(self, group_name, func):
        Group.objects.get_or_create(name=group_name)

        self.groups[group_name] = func

    def activate_group(self, feature_name, group_name):
        feature = get_feature_or_raise_error(feature_name)

        get_group_or_raise_error(group_name).features.add(feature)

    def feature_enabled_for_actor(self, feature, actor):
        return actor and (
            self.feature_enabled_for_a_group_of_actor(feature, actor) or feature.has_actor(actor.flip_id())
        )

    def feature_enabled_for_a_group_of_actor(self, feature, actor):
        groups_names = [group.name for group in feature.group_set.all()]
        return any(self.groups[group_name](actor) for group_name in groups_names)

    def enable_actor(self, feature_name, actor):
        feature = Feature.objects.filter(name=feature_name).first()
        flip_id = actor.flip_id()

        return feature.add_actor(flip_id)


def get_feature_or_raise_error(feature_name):
    try:
        return Feature.objects.get(name=feature_name)
    except Feature.DoesNotExist:
        raise FeatureFlip.FeatureFlipError(f'Feature {feature_name} does not exist')


def get_group_or_raise_error(group_name):
    try:
        return Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        raise FeatureFlip.FeatureFlipError(f'Group {group_name} does not exist')
