from rest_framework import generics

from apps.map.models import Map
from apps.map.serialziers.map_serializer import MapSerializer


class MapView(generics.RetrieveAPIView):
    queryset = Map.objects.all()
    serializer_class = MapSerializer
    lookup_field = "map_type"
