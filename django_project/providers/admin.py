from django.contrib import admin

from .models import ProviderStatus, Provider, ProviderResponse


class ProviderStatusAdmin(admin.ModelAdmin):
    pass

admin.site.register(ProviderStatus, ProviderStatusAdmin)


class ProviderAdmin(admin.ModelAdmin):
    pass

admin.site.register(Provider, ProviderAdmin)


class ProviderResponseAdmin(admin.ModelAdmin):
    pass

admin.site.register(ProviderResponse, ProviderResponseAdmin)
