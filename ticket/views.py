from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404

from ticket.models import Maintenance, Incident, Update


def maintenance_detail(request, pk):
    updates_prefetch = Prefetch("updates", queryset=Update.objects.order_by("-created_at"))
    maintenance = get_object_or_404(
        Maintenance.objects.select_related("service").prefetch_related(updates_prefetch), pk=pk
    )
    return render(
        request,
        "maintenance_detail.html",
        {"maintenance": maintenance, "service": maintenance.service, "updates": maintenance.updates.all()},
    )


def incident_detail(request, pk):
    updates_prefetch = Prefetch(
        "updates",
        queryset=Update.objects.order_by("-created_at"),
        # Order updates by created_at
    )
    incident = get_object_or_404(Incident.objects.select_related("service").prefetch_related(updates_prefetch), pk=pk)
    return render(
        request,
        "incident_detail.html",
        {"incident": incident, "service": incident.service, "updates": incident.updates.all()},
    )
