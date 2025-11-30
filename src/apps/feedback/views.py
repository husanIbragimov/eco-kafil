from rest_framework import generics
from apps.feedback.models import Feedback
from apps.feedback.serializers import FeedbackSerializer


class FeedbackCreateView(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
