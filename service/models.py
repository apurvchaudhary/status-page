from django.db import models
from django.db.models.manager import Manager
from account.models import CustomUser


class Service(models.Model):
    STATUS_CHOICES = [
        ("Operational", "Operational"),
        ("Degraded Performance", "Degraded Performance"),
        ("Partial Outage", "Partial Outage"),
        ("Major Outage", "Major Outage"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Operational")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="services_created_by")
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="services_updated_by")

    objects = Manager()

    def __str__(self):
        return self.name
