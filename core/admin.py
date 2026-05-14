from django.contrib import admin
from .models import (
    Project,
    Resource,
    Summary,
    Tag,
    ResourceTag,
    Comparison,
    ComparisonItem
)

admin.site.register(Project)
admin.site.register(Resource)
admin.site.register(Summary)
admin.site.register(Tag)
admin.site.register(ResourceTag)
admin.site.register(Comparison)
admin.site.register(ComparisonItem)