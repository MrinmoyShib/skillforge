"""
Seed command to populate initial platform achievements with multi-language track badges.
"""
from django.core.management.base import BaseCommand
from apps.problems.models import Category
from apps.achievements.models import Achievement


class Command(BaseCommand):
    help = "Seeds initial platform achievements and language track badges."

    def handle(self, *args, **options):
        self.stdout.write("Seeding achievements...")

        py_cat = Category.objects.filter(slug="python").first()
        js_cat = Category.objects.filter(slug="javascript").first()
        cpp_cat = Category.objects.filter(slug="cpp").first()

        achievements_data = [
            {
                "name": "First Blood",
                "slug": "first-blood",
                "description": "Solve your very first coding challenge on SkillForge.",
                "icon": "⚔️",
                "criteria_type": Achievement.CriteriaType.FIRST_SOLVE,
                "criteria_value": 1,
                "xp_bonus": 25,
            },
            {
                "name": "Streak Starter",
                "slug": "streak-starter",
                "description": "Maintain a 3-day active problem-solving streak.",
                "icon": "🔥",
                "criteria_type": Achievement.CriteriaType.STREAK_DAYS,
                "criteria_value": 3,
                "xp_bonus": 50,
            },
            {
                "name": "Problem Solver",
                "slug": "problem-solver",
                "description": "Successfully master 5 unique coding challenges.",
                "icon": "💡",
                "criteria_type": Achievement.CriteriaType.PROBLEMS_COUNT,
                "criteria_value": 5,
                "xp_bonus": 50,
            },
            {
                "name": "Algorithm Apprentice",
                "slug": "algorithm-apprentice",
                "description": "Master 10 coding challenges across the platform.",
                "icon": "🧠",
                "criteria_type": Achievement.CriteriaType.PROBLEMS_COUNT,
                "criteria_value": 10,
                "xp_bonus": 100,
            },
            {
                "name": "Rising Star",
                "slug": "rising-star",
                "description": "Advance your telemetry and reach Level 2 (Junior Coder).",
                "icon": "⭐",
                "criteria_type": Achievement.CriteriaType.LEVEL_REACHED,
                "criteria_value": 2,
                "xp_bonus": 50,
            },
            {
                "name": "Master Architect",
                "slug": "master-architect",
                "description": "Reach Level 5 (Architect) by mastering hard challenges.",
                "icon": "👑",
                "criteria_type": Achievement.CriteriaType.LEVEL_REACHED,
                "criteria_value": 5,
                "xp_bonus": 200,
            },
        ]

        if py_cat:
            achievements_data.append({
                "name": "Python Pioneer",
                "slug": "python-pioneer",
                "description": "Master 2 challenges in the Python Track.",
                "icon": "🐍",
                "criteria_type": Achievement.CriteriaType.CATEGORY_SOLVE,
                "criteria_value": 2,
                "criteria_category": py_cat,
                "xp_bonus": 50,
            })

        if js_cat:
            achievements_data.append({
                "name": "JavaScript Ninja",
                "slug": "javascript-ninja",
                "description": "Master 2 challenges in the JavaScript Track.",
                "icon": "🟨",
                "criteria_type": Achievement.CriteriaType.CATEGORY_SOLVE,
                "criteria_value": 2,
                "criteria_category": js_cat,
                "xp_bonus": 50,
            })

        if cpp_cat:
            achievements_data.append({
                "name": "C++ Systems Veteran",
                "slug": "cpp-veteran",
                "description": "Master 2 challenges in the C++ Track.",
                "icon": "⚡",
                "criteria_type": Achievement.CriteriaType.CATEGORY_SOLVE,
                "criteria_value": 2,
                "criteria_category": cpp_cat,
                "xp_bonus": 50,
            })

        created_count = 0
        updated_count = 0

        for data in achievements_data:
            obj, created = Achievement.objects.update_or_create(
                slug=data["slug"],
                defaults=data
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded achievements ({created_count} created, {updated_count} updated)."
            )
        )
