from django.db.models import Count, Q
from django.utils import timezone

from service_provider.models import ServiceProvider


class FreeBookingTimes:

    def __init__(self, day):
        self.day = day
        self.opening = ""
        self.closing = ""
        self.free_times = []

    def set_opening_hours(self, opening, closing):
        self.opening = opening
        self.closing = closing

    def add_free_time(self, free_time):
        self.free_times.append(free_time)

def get_service_providers_sorted_by_user_bookings(user_profile):
    providers = ServiceProvider.objects.filter(
        expired_date__gte=timezone.now()
    ).annotate(
        user_booking_count=Count(
            'bookings',
            filter=Q(bookings__booked_user=user_profile)
        )
    ).order_by('-user_booking_count', 'name')  # Másodlagos rendezés név szerint
    return providers
