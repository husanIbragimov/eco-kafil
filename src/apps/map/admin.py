from django.contrib import admin

from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget

from apps.map.models import Map

@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }
