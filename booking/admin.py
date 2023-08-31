from django.contrib import admin

from booking.models import Booking


class BookingAdmin(admin.ModelAdmin):
    list_display = ['booked_user', 'service', 'start_time', 'end_time','length','is_accept']


# Register your models here.
admin.site.register(Booking, BookingAdmin)
