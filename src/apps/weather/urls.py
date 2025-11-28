from django.urls import path

from .views import WeatherView

urlpatterns = [
    path("weakly/", WeatherView.as_view(), name="daily-weather"),
]
