from django.contrib import admin
from django.db.models import Q

from account.models import Organization, CustomUser, Team

admin.site.site_header = "Dashboard"
admin.site.site_title = "state manager admin"
admin.site.index_title = ""
admin.site.site_url = "/"


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "team", "created_at")

    def get_queryset(self, request):
        # Superuser can access all organizations
        if request.user.is_superuser:
            return super().get_queryset(request)

        # Admin can only access organizations they own or are part of the team
        if request.user.role == "admin":
            return Organization.objects.filter(Q(owner=request.user) | Q(team__members=request.user)).distinct()

        # If the user is member, they have limited access to team's organizations
        return Organization.objects.filter(team__members=request.user).distinct()


class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")

    def get_queryset(self, request):
        # Superuser can access all teams
        if request.user.is_superuser:
            return super().get_queryset(request)
        return Team.objects.filter(members=request.user)


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(CustomUser)
