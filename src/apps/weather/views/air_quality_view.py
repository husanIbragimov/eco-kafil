from datetime import datetime

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.station.models import Station
from apps.weather.models import Weather
from apps.weather.serializers import WeatherSerializer


class WeatherDailyView(ListAPIView):
    """
    API endpoint to get daily weather data for all 13 regions.
    Returns weather data grouped by region code.
    Only returns data for stations where parent_id is NULL (regions only).
    """
    serializer_class = WeatherSerializer

    def get_queryset(self):
        # Get today's date
        today = datetime.now().date()

        # Get latest weather data for each region for today
        # Filter by station__parent__isnull=True to get only regions (not districts or villages)
        queryset = Weather.objects.filter(
            station__parent__isnull=True,  # Only parent stations (regions, where parent_id is NULL)
            date=today
        ).select_related('station').order_by('-id')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Group data by region code in the format: {"code": {weather_data}}
        result = {}
        for item in serializer.data:
            region_code = str(item.pop('region_code'))
            result[region_code] = item

        return Response(result)


class WeatherDetailView(APIView):
    """
    API endpoint to get daily weather data for a specific region by code.
    Returns weather data for the region with the given code for today.
    Only returns data for stations where parent_id is NULL (regions only).

    URL: /weather/daily/<region_code>/
    Example: /weather/daily/1700000000/
    """

    def get(self, request, region_code):
        # Get today's date
        today = datetime.now().date()

        # Validate region code exists and is a parent station (region)
        try:
            station = Station.objects.get(code=region_code, parent__isnull=True)
        except Station.DoesNotExist:
            return Response(
                {"error": f"Region with code {region_code} not found or is not a valid region"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get weather data for this region for today
        try:
            weather = Weather.objects.filter(
                station=station,
                date=today
            ).select_related('station').latest('id')
        except Weather.DoesNotExist:
            return Response(
                {"error": f"No weather data found for region {region_code} for today"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Serialize and return the data
        serializer = WeatherSerializer(weather)
        data = serializer.data

        # Remove region_code and region_name from response (optional, since we already know it)
        data.pop('region_code', None)
        data.pop('region_name', None)

        return Response(data)


class WeeklyWeatherView(ListAPIView):
    """
    API endpoint to get weekly weather data for all 13 regions.
    """
    serializer_class = WeatherSerializer

    def get_queryset(self):
        queryset = Weather.objects.filter(
            station__parent__isnull=True  # Only parent stations (regions)
        ).select_related('station').order_by('-id')[:91]  # 13 regions * 7 days

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
