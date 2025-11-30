from django.urls import path

from apps.feedback.views import FeedbackCreateView

urlpatterns = [
    path("create", FeedbackCreateView.as_view(), name="create-feedback")
]
