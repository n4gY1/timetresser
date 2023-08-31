import uuid

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from account.models import UserProfile, User


@receiver(pre_save, sender=UserProfile)
def delete_old_profile_picture(sender, instance, **kwargs):
    if instance.pk:  # Ellenőrzi, hogy a rekord már létezik (nem új létrehozás)
        try:
            old_instance = UserProfile.objects.get(pk=instance.pk)
            if old_instance.profile_picture and old_instance.profile_picture != instance.profile_picture:
                old_instance.profile_picture.delete(save=False)
        except UserProfile.DoesNotExist:
            pass


@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        print('created new profile')
        UserProfile.objects.create(user=instance)
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            print("not success edit, creating userprofile")
            UserProfile.objects.create(user=instance)
