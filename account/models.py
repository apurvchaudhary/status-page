from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    ROLE_CHOICES = [("superuser", "Superuser"), ("admin", "Admin"), ("member", "Member")]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")

    def __str__(self):
        return f"{self.username}"

    def save(self, *args, **kwargs):
        if self.role == "admin" and not self.pk:
            super().save(*args, **kwargs)
            group = Group.objects.get(name="admin")
            self.groups.add(group)
        if self.role == "member" and not self.pk:
            super().save(*args, **kwargs)
            group = Group.objects.get(name="member")
            self.groups.add(group)
        super().save(*args, **kwargs)
