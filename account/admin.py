from django.contrib import admin

from account.models import CustomUser

admin.site.site_header = "Dashboard"
admin.site.site_title = "state manager admin"
admin.site.index_title = ""
admin.site.site_url = "/"

admin.site.register(CustomUser)
