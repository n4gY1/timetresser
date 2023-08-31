import datetime

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from service_provider.models import ServiceProvider


@receiver(pre_save, sender=ServiceProvider)
def add_expired_date_when_created(sender, instance, **kwargs):
    if instance.pk is None:
        instance.expired_date = datetime.datetime.now() + datetime.timedelta(days=31)
    else:
        instance.slug = slugify(instance.name)
