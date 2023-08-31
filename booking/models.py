from django.db import models

from account.models import UserProfile
from service_provider.models import ServiceProvider


# Create your models here.
class Booking(models.Model):
    booked_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name="my_bookings")
    service = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE,related_name="bookings")
    start_time = models.DateTimeField()
    description = models.TextField()
    accept_description = models.TextField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    length = models.PositiveSmallIntegerField(null=True, blank=True)
    is_accept = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

