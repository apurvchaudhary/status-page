from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.manager import Manager


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    ROLE_CHOICES = [("superuser", "Superuser"), ("admin", "Organization Admin"), ("member", "Member")]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")

    def __str__(self):
        return f"{self.username}"

    def save(self, *args, **kwargs):
        if self.role == "admin" and not self.pk:
            super().save(*args, **kwargs)
            group = Group.objects.get(name="Organization-Admin")
            self.groups.add(group)
        if self.role == "member" and not self.pk:
            super().save(*args, **kwargs)
            group = Group.objects.get(name="Organization-Member")
            self.groups.add(group)
        super().save(*args, **kwargs)


class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(CustomUser, related_name="teams")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = Manager()

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="owned_organizations")
    team = models.OneToOneField(Team, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = Manager()

    def __str__(self):
        return self.name
