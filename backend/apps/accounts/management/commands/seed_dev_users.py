"""
Management command to create initial development users (Admin and Student).
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.accounts.services.auth_services import user_register

User = get_user_model()


class Command(BaseCommand):
    help = "Seeds development admin and student users."

    def handle(self, *args, **options):
        # 1. Seed Admin
        admin_user = User.objects.filter(username="admin").first()
        if not admin_user:
            admin_user = user_register(
                username="admin",
                email="admin@skillforge.dev",
                password="AdminPassword123!",
                display_name="SkillForge Administrator"
            )
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save(update_fields=['is_staff', 'is_superuser'])
            self.stdout.write(self.style.SUCCESS("Created admin user: admin / AdminPassword123!"))
        else:
            self.stdout.write("Admin user already exists.")

        # 2. Seed Student
        student_user = User.objects.filter(username="student").first()
        if not student_user:
            user_register(
                username="student",
                email="student@skillforge.dev",
                password="StudentPassword123!",
                display_name="Alex River"
            )
            self.stdout.write(self.style.SUCCESS("Created student user: student / StudentPassword123!"))
        else:
            self.stdout.write("Student user already exists.")

