from django.urls import path

from service import views

urlpatterns = [
    path("", views.service_list, name="service_list"),
    path("service/<int:pk>/", views.service_detail, name="service_detail"),
    path("status/<int:pk>/", views.service_status, name="service_status"),
]
