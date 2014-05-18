from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import RequestStatus, CustomUser


class CustomUserAdmin(UserAdmin):
    pass

admin.site.register(CustomUser, CustomUserAdmin)


class RequestStatusAdmin(admin.ModelAdmin):
    pass

admin.site.register(RequestStatus, RequestStatusAdmin)
