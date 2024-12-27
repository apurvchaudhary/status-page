from django.db import models
from django.db.models.manager import Manager
from django.utils.timezone import now

from account.models import CustomUser
from service.models import Service


class Incident(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="incidents")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,
                                   related_name="incidents_created_by")
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,
                                   related_name="incidents_updated_by")

    objects = Manager()

    def __str__(self):
        return self.title


class Maintenance(models.Model):
    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="scheduled")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="maintenances")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name="maintenances_created_by"
    )
    updated_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name="maintenances_updated_by"
    )

    objects = Manager()

    def __str__(self):
        return self.title


class Update(models.Model):
    update_text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=now)
    status = models.CharField(max_length=25, null=True, blank=True)
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name="updates", null=True, blank=True)
    maintenance = models.ForeignKey(
        Maintenance, on_delete=models.CASCADE, related_name="updates", null=True, blank=True
    )
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    objects = Manager()

    def __str__(self):
        return f"Update at {self.created_at}"
