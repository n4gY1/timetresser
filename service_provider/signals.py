import datetime
import os

from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.utils.text import slugify

from service_provider.models import ServiceProvider, ServiceProviderPicture


@receiver(pre_save, sender=ServiceProvider)
def add_expired_date_when_created(sender, instance, **kwargs):
    if instance.pk is None:
        instance.expired_date = datetime.datetime.now() + datetime.timedelta(days=31)
    else:
        instance.slug = slugify(instance.name)
        try:
            old_service = sender.objects.get(pk=instance.pk)
            if not old_service.banner_picture == instance.banner_picture:
                os.remove(old_service.banner_picture.path)
        except Exception as e:
            print("[ERROR]", e)


@receiver(pre_delete, sender=ServiceProviderPicture)
def delete_service_refer_picture(sender, instance, **kwargs):
    instance.image.delete()
