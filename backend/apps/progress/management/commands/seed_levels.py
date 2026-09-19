"""
Seed command to populate initial LevelRequirement progression thresholds.
"""
from django.core.management.base import BaseCommand
from apps.progress.models import LevelRequirement

TIERS = [
    {"level": 1, "xp_threshold": 0, "title": "Apprentice"},
    {"level": 2, "xp_threshold": 100, "title": "Junior Coder"},
    {"level": 3, "xp_threshold": 250, "title": "Practitioner"},
    {"level": 4, "xp_threshold": 500, "title": "Specialist"},
    {"level": 5, "xp_threshold": 1000, "title": "Architect"},
    {"level": 6, "xp_threshold": 1750, "title": "Grandmaster"},
    {"level": 7, "xp_threshold": 2750, "title": "Legend"},
]


class Command(BaseCommand):
    help = "Seeds LevelRequirement tiers into the database."

    def handle(self, *args, **options):
        self.stdout.write("Seeding level requirements...")
        created_count = 0
        updated_count = 0

        for tier in TIERS:
            obj, created = LevelRequirement.objects.update_or_create(
                level=tier["level"],
                defaults={
                    "xp_threshold": tier["xp_threshold"],
                    "title": tier["title"],
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded level requirements ({created_count} created, {updated_count} updated)."
            )
        )

