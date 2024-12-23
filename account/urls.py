from django.urls import path

from account import views

urlpatterns = [
    path("admin-signup/", views.admin_signup, name="signup"),
]
