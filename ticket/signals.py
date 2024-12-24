from django.db.models.signals import post_save
from django.dispatch import receiver

from ticket.models import Incident, Maintenance, Service
from ticket.tasks import send_model_updates


@receiver(post_save, sender=Service)
@receiver(post_save, sender=Incident)
@receiver(post_save, sender=Maintenance)
def handle_tickets(sender, instance, created, **kwargs):
    send_model_updates.delay(instance.id, sender.__name__, created, getattr(instance, "remark", None))
