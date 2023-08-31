from django.contrib import admin

from service_provider.models import ServiceProvider, ServiceProviderPicture, ServiceProviderOpeningHours


class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'user_profile', 'expired_date']


class ServiceProviderOpeningHoursAdmin(admin.ModelAdmin):
    list_display = ['service_provider', 'day', 'start_time', 'end_time']


# Register your models here.
admin.site.register(ServiceProvider, ServiceProviderAdmin)
admin.site.register(ServiceProviderPicture)
admin.site.register(ServiceProviderOpeningHours, ServiceProviderOpeningHoursAdmin)
