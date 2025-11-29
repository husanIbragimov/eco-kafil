from django.urls import path

from .views import (
    MapView,
)

urlpatterns = [
    path("<int:map_type>/", MapView.as_view(), name="station-detail"),
]
