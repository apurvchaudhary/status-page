from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "get or create default groups with specific permissions"

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Organization-Admin")
        if created:
            permissions = Permission.objects.filter(
                codename__in=[
                    "add_organization",
                    "change_organization",
                    "delete_organization",
                    "view_organization",
                    "add_team",
                    "change_team",
                    "delete_team",
                    "view_team",
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
            self.stdout.write(self.style.SUCCESS(f"Group Organization-Admin created successfully"))
        group, created = Group.objects.get_or_create(name="Organization-Member")
        if created:
            permissions = Permission.objects.filter(
                codename__in=[
                    "view_organization",
                    "view_team",
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
            self.stdout.write(self.style.SUCCESS(f"Group Organization-Member created successfully"))
