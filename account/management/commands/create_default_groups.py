from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "get or create default groups with specific permissions"

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="admin")
        if created:
            permissions = Permission.objects.filter(
                codename__in=[
                    "add_service",
                    "change_service",
                    "delete_service",
                    "view_service",
                    "add_maintenance",
                    "change_maintenance",
                    "delete_maintenance",
                    "view_maintenance",
                    "add_incident",
                    "change_incident",
                    "delete_incident",
                    "view_incident",
                ]
            )
            group.permissions.set(permissions)
            self.stdout.write(self.style.SUCCESS(f"Group Admin created successfully"))
        group, created = Group.objects.get_or_create(name="member")
        if created:
            permissions = Permission.objects.filter(
                codename__in=[
                    "add_service",
                    "change_service",
                    "view_service",
                    "add_maintenance",
                    "change_maintenance",
                    "view_maintenance",
                    "add_incident",
                    "change_incident",
                    "view_incident",
                ]
            )
            group.permissions.set(permissions)
            group.save()
            self.stdout.write(self.style.SUCCESS(f"Group Member created successfully"))
