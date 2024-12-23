from django.urls import path
from ticket import views


urlpatterns = [
    path("incident/<int:pk>/", views.incident_detail, name="incident_detail"),
    path("maintenance/<int:pk>/", views.maintenance_detail, name="maintenance_detail"),
]
