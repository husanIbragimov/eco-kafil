from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from apps.station.models import Station
from apps.weather.models import Weather




class WeatherResource(resources.ModelResource):
    hudud = fields.Field(
        column_name='hudud',
        attribute='station',
        widget=ForeignKeyWidget(Station, field='code')
    )

    class Meta:
        model = Weather
        fields = (
            'hudud', 'temperature', 'humidity', 'wind_speed',
            'pressure', 'precipitation', 'pm2_5', 'pm10', 'fog', 'aqi', 'date'
        )
        import_id_fields = []
        skip_unchanged = True
        report_skipped = True

    def before_import_row(self, row, row_number=None, **kwargs):
        """Excel fayldan ma'lumotlarni import qilishdan oldin tekshirish"""
        # Agar hudud code bo'sh bo'lsa, station None bo'ladi
        if not row.get('hudud'):
            row['hudud'] = None
        return row
