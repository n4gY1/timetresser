import datetime

from django.db.models.signals import pre_save
from django.dispatch import receiver

from booking.models import Booking



@receiver(pre_save, sender=Booking)
def post_save_booking_receiver(sender, instance, **kwargs):
    if instance.length:
        booking = instance
        length = booking.length
        end_time = booking.start_time + datetime.timedelta(minutes=length)
        booking.end_time = end_time

