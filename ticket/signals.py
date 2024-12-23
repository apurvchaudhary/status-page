from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from ticket.models import Incident, Maintenance, Service


@receiver(post_save, sender=Incident)
@receiver(post_save, sender=Maintenance)
def handle_tickets(sender, instance, created, **kwargs):
    message = {"service_id": str(instance.service_id)}
    if isinstance(instance, Incident):
        message["incident_id"] = instance.id
        message["message"] = (
            f"{instance.created_by if created else instance.updated_by}"
            f" {'created' if created else 'updated'} incident"
            f" {instance.title}"
        )
    elif isinstance(instance, Maintenance):
        message["maintenance_id"] = instance.id
        message["message"] = (
            f"{instance.created_by if created else instance.updated_by}"
            f" {'created' if created else 'updated'} maintenance"
            f" {instance.title}"
        )
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("updates", {"type": "send_update", "message": message})


@receiver(post_save, sender=Service)
def handle_service_changes(sender, instance, created, **kwargs):
    message = {
        "organization_id": instance.organization_id,
        "service_id": instance.id,
        "message": f" {'created' if created else 'updated'} service {instance.name}",
    }
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("updates", {"type": "send_update", "message": message})
