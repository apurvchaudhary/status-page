from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from service.models import Service
from service.serializers import ServiceSerializer
from ticket.models import Incident, Maintenance


def service_list(request):
    return render(request, "service_list.html", {"services": Service.objects.all()})


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    incidents = service.incidents.filter(
        status__in=[Incident.STATUS_CHOICES[0][0], Incident.STATUS_CHOICES[1][0]]
    ).order_by("-created_at")
    maintenances = service.maintenances.filter(
        status__in=[Maintenance.STATUS_CHOICES[0][0], Maintenance.STATUS_CHOICES[1][0]]
    ).order_by("-start_time")
    return render(
        request,
        "service_detail.html",
        {
            "service": service,
            "incidents": incidents,
            "maintenances": maintenances,
        },
    )


@api_view(["GET"])
def service_info(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return Response(ServiceSerializer(service).data)
