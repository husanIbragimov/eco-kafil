import json

from django.conf import settings
from django.core.management.base import BaseCommand
from tqdm import tqdm

from apps.station.models import Station


class Command(BaseCommand):
    help = "Load SOATO data from JSON file into the database"

    def handle(self, *args, **options):
        data = self.load_json()
        is_exists, err = self.exists(data)
        if is_exists:
            self.stdout.write(self.style.WARNING(f"{err}"))
        elif self.insert(data):
            self.stdout.write(self.style.SUCCESS("SOATO data successfully loaded."))
        else:
            self.stdout.write(self.style.ERROR("Failed to load SOATO data."))

    @staticmethod
    def load_json() -> dict:
        with open(f"{settings.BASE_DIR.parent}/assets/soato.json", "r", encoding="utf-8") as file:
            data = json.loads(file.read())
            return data

    @staticmethod
    def exists(soato: dict) -> tuple[bool, str]:
        total = len(soato)
        for item in soato:
            total += len(item["children"])
            if "children" in item:
                for district in item["children"]:
                    total += len(district.get("children", []))
        total_objs = Station.objects.count()
        if total_objs == total:
            return True, f"{total} SOATO records already exist in the database "
        if 0 < total_objs < total:
            return (
                True,
                f"{total} SOATO records do not exist in the database, need to insert {total - total_objs} records",
            )
        return False, "No SOATO records found in the database, ready to insert all records."

    @staticmethod
    def insert(soato: dict):
        regions = []
        districts = []

        for item in tqdm(soato, desc="Processing Regions"):
            region = Station(
                title=dict(uz=item["name_uz"], ru=item["name_ru"]),
                name=item["name_uz"],
                code=item["soato_id"],
            )
            regions.append(region)


            for district in tqdm(item["children"], desc=f"Processing Districts of {item['name_uz']}", leave=False):
                district_obj = Station(
                    title=dict(uz=district["name_uz"], ru=district["name_ru"]),
                    name=district["name_uz"],
                    code=district["soato_id"],
                    parent=region
                )
                districts.append(district_obj)

                # Progress bar for villages within each district
                # if 'children' in district:
                #     for village in tqdm(district['children'], desc=f"Processing Villages of {district['name_uz']}",
                #                         leave=False):
                #         village_obj = Area(
                #             title=dict(
                #                 uz=village['name_uz'],
                #                 ru=village['name_ru']
                #             ),
                #             parent=district_obj
                #         )
                #         villages.append(village_obj)

        Station.objects.bulk_create(regions)
        Station.objects.bulk_create(districts)
        # Station.objects.bulk_create(villages)
        return True
