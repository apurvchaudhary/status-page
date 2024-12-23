from django.db import models
from django.db.models.manager import Manager

from account.models import Organization


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
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="services")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = Manager()

    def __str__(self):
        return self.name
