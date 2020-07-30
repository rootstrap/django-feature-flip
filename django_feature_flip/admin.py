from django.contrib import admin
from django_feature_flip.models import Feature


class FeatureAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'totally_enabled',
    )


admin.site.register(Feature, FeatureAdmin)
