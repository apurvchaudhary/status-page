from django.urls import path

from service import views

urlpatterns = [
    path("", views.service_list, name="service_list"),
    path("service/<int:pk>/", views.service_detail, name="service_detail"),
    path("service/info/<int:pk>/", views.service_info, name="service_status"),
]
