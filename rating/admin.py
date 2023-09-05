from django.contrib import admin

from rating.models import Rating


# Register your models here.
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'service_provider', 'created_at', 'rate', 'description']


admin.site.register(Rating, RatingAdmin)
