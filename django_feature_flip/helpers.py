from django_feature_flip.models import Feature


class FeatureFlip:
    class __FeatureFlip:
        def __init__(self):
            pass

        def __str__(self):
            return repr(self)

    instance = None

    def __init__(self):
        if not FeatureFlip.instance:
            FeatureFlip.instance = FeatureFlip.__FeatureFlip()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def enabled(self, feature_name, actor=None):
        return Feature.objects.get(name=feature_name).enabled(actor)
