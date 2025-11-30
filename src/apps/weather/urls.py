from django.urls import path

from .views import WeatherView, WeeklyWeatherView, WeatherDailyView, WeatherDetailView

urlpatterns = [
    path("daily/", WeatherDailyView.as_view(), name="daily-weather"),
    path("daily/<str:region_code>/", WeatherDetailView.as_view(), name="daily-weather-detail"),
    path("weakly/", WeatherView.as_view(), name="weekly-weather"),
    path("weekly/", WeeklyWeatherView.as_view(), name="weekly-weather"),
]
