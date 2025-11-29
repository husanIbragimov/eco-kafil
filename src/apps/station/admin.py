from django.contrib import admin

from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget

from apps.station.models import Station

@admin.register(Station)
class MapAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }
