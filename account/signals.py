from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import CustomUser


@receiver(post_save, sender=CustomUser)
def create_organization_environment(sender, instance, created, **kwargs):
    if created:
        pass
