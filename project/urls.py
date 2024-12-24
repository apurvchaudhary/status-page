"""
URL configuration for project
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView


urlpatterns = [
    # accounts app urls
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),
    # service app urls
    path("", include("service.urls")),
    path("ticket/", include("ticket.urls")),
    # favicon for site
    path("favicon.ico", RedirectView.as_view(url="/static/images/favicon.png")),
]
handler403 = "account.exception_handler.handler403"
handler404 = "account.exception_handler.handler404"
