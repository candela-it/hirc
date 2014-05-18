from django.contrib import admin

from .models import RequestStatus


class RequestStatusAdmin(admin.ModelAdmin):
    pass

admin.site.register(RequestStatus, RequestStatusAdmin)
