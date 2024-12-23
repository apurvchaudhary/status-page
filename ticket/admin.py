from django import forms
from django.contrib import admin
from django.db.models import Q
from django.utils import timezone

from ticket.models import Incident, Maintenance, Update, Service


class IncidentAdminForm(forms.ModelForm):
    remark = forms.CharField(widget=forms.Textarea, required=False, help_text="Add Comment to this update")

    class Meta:
        model = Incident
        fields = ["title", "description", "status", "service"]


class MaintenanceAdminForm(forms.ModelForm):
    remark = forms.CharField(widget=forms.Textarea, required=False, help_text="Add Comment to this update")

    class Meta:
        model = Maintenance
        fields = ["title", "description", "status", "service", "start_time", "end_time"]


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    form = IncidentAdminForm
    list_display = ("title", "description", "status", "service")
    search_fields = ("title", "status")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            Update.objects.create(
                incident=obj,
                status=obj.status,
                update_text=form.cleaned_data.get("remark"),
                created_at=timezone.now(),
                updated_by=request.user,
            )
        obj.updated_by = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Restrict services based on the logged-in user
        if not request.user.is_superuser:
            form.base_fields["service"].queryset = Service.objects.filter(
                Q(organization__owner=request.user) | Q(organization__team__members=request.user)
            ).distinct()
            if obj:
                form.base_fields["service"].disabled = True
            else:
                form.base_fields["status"].disabled = True
        return form

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        elif request.user.role == "admin":
            return Incident.objects.filter(
                Q(service__organization__owner=request.user) | Q(service__organization__team__members=request.user)
            ).distinct()
        return Incident.objects.filter(service__organization__team__members=request.user).distinct()


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    form = MaintenanceAdminForm
    list_display = ("title", "description", "status", "service", "start_time", "end_time")
    search_fields = ("title", "status")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            Update.objects.create(
                maintenance=obj,
                status=obj.status,
                update_text=form.cleaned_data.get("remark"),
                created_at=timezone.now(),
                updated_by=request.user,
            )
        obj.updated_by = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Restrict services based on the logged-in user
        if not request.user.is_superuser:
            form.base_fields["service"].queryset = Service.objects.filter(
                Q(organization__owner=request.user) | Q(organization__team__members=request.user)
            ).distinct()
            if obj:
                form.base_fields["service"].disabled = True
            else:
                form.base_fields["status"].disabled = True
        return form

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        elif request.user.role == "admin":
            return Maintenance.objects.filter(
                Q(service__organization__owner=request.user) | Q(service__organization__team__members=request.user)
            ).distinct()
        return Maintenance.objects.filter(service__organization__team__members=request.user).distinct()
