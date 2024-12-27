from django import forms
from django.contrib import admin

from ticket.models import Incident, Maintenance


def set_save_context(obj, change, request, form):
    if not change:
        obj.created_by = request.user
    obj.updated_by = request.user
    obj.remark = form.cleaned_data.get("remark")


def set_form_context(obj, form):
    if obj:
        form.base_fields["service"].disabled = True
    else:
        form.base_fields["status"].disabled = True
    return form


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
        set_save_context(obj, change, request, form)
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return set_form_context(obj, form)


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    form = MaintenanceAdminForm
    list_display = ("title", "description", "status", "service", "start_time", "end_time")
    search_fields = ("title", "status")

    def save_model(self, request, obj, form, change):
        set_save_context(obj, change, request, form)
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return set_form_context(obj, form)
