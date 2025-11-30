from django.urls import include, path

urlpatterns = [
    path(
        "auth/",
        include(("apps._auth.urls.auth_urls", "auth"), namespace="auth"),
    ),
    path(
        "user/",
        include(("apps._auth.urls.user_urls", "user"), namespace="user"),
    ),
    path("upload/", include(("apps.upload.urls", "upload"), namespace="upload")),
    path("station/", include(("apps.station.urls", "station"), namespace="station")),
    path("weather/", include(("apps.weather.urls", "weather"), namespace="weather")),
    path("feedback/", include(("apps.feedback.urls", "feedback"), namespace="feedback")),
]
