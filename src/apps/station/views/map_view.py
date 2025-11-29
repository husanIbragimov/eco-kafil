from rest_framework import generics

from apps.common.serializers import EmptySerializer
from apps.station.models import Station


class MapView(generics.RetrieveAPIView):
    queryset = Station.objects.all()
    serializer_class = EmptySerializer
    lookup_field = "map_type"
