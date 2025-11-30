import random
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.station.models import Station
from apps.weather.models import Weather


class Command(BaseCommand):
    help = "Generate daily weather data for all 13 regions"

    # SOATO codes for 13 regions of Uzbekistan
    REGION_CODES = [
        "1700000000",  # Tashkent city
        "0600000000",  # Namangan region
        "1400000000",  # Tashkent region
        "0300000000",  # Fergana region
        "0100000000",  # Andijan region
        "1200000000",  # Syrdarya region
        "0700000000",  # Jizzakh region
        "0900000000",  # Navoi region
        "1000000000",  # Samarkand region
        "0800000000",  # Kashkadarya region
        "1300000000",  # Surkhandarya region
        "0200000000",  # Bukhara region
        "0400000000",  # Khorezm region
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=1,
            help='Number of days to generate weather data for (default: 1)'
        )

    def handle(self, *args, **options):
        days = options['days']

        # Get all region stations
        regions = Station.objects.filter(code__in=self.REGION_CODES, parent__isnull=True)

        if regions.count() != 13:
            self.stdout.write(
                self.style.WARNING(
                    f"Expected 13 regions, found {regions.count()}. Make sure SOATO data is loaded."
                )
            )
            return

        # Generate weather data for each day
        for day_offset in range(days):
            date = timezone.now().date() - timedelta(days=day_offset)

            # Check if data already exists for this date
            existing_count = Weather.objects.filter(
                station__code__in=self.REGION_CODES,
                created_at__date=date
            ).count()

            if existing_count >= 13:
                self.stdout.write(
                    self.style.WARNING(
                        f"Weather data for {date} already exists. Skipping..."
                    )
                )
                continue

            weather_records = []

            for region in regions:
                weather_data = self.generate_weather_data(region)
                weather_records.append(weather_data)

            Weather.objects.bulk_create(weather_records)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully generated weather data for {date} ({len(weather_records)} regions)"
                )
            )

    def generate_weather_data(self, station):
        """Generate random but realistic weather data for a region"""

        # Generate realistic weather values
        humidity = round(random.uniform(55, 80), 1)
        temperature = round(random.uniform(5, 15), 1)
        wind_speed = round(random.uniform(2.0, 5.0), 1)
        pressure = round(random.uniform(1010, 1018), 1)
        precipitation = round(random.choice([0, 0, 0, 0.3, 0.5, 1.2]), 1)

        # PM2.5 and PM10 values
        pm2_5 = round(random.uniform(15, 50), 1)
        pm10 = round(random.uniform(20, 95), 1)

        # Fog (0 or 1)
        fog = 1 if precipitation > 0 and humidity > 70 else 0

        # Calculate AQI based on PM values
        aqi = round(max(pm2_5 * 2.3, pm10 * 0.9))

        return Weather(
            station=station,
            station_name=station.name,
            humidity=humidity,
            temperature=temperature,
            wind_speed=wind_speed,
            pressure=pressure,
            precipitation=precipitation,
            pm2_5=pm2_5,
            pm10=pm10,
            fog=fog,
            aqi=aqi,
        )
