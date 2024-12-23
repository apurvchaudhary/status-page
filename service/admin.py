from django.contrib import admin
from django.db.models import Q

from service.models import Organization
from service.models import Service


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "created_at")

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        elif request.user.role == "admin":
            return Service.objects.filter(
                Q(organization__owner=request.user) | Q(organization__team__members=request.user)
            ).distinct()
        return Service.objects.filter(organization__team__members=request.user).distinct()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Restrict organizations based on the logged-in user
        if not request.user.is_superuser:
            form.base_fields["organization"].queryset = Organization.objects.filter(
                Q(owner=request.user) | Q(team__members=request.user)
            ).distinct()
        if obj:
            form.base_fields["organization"].disabled = True
        return form


admin.site.register(Service, ServiceAdmin)
