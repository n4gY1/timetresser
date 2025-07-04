import uuid

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from account.models import UserProfile, User
import os

@receiver(pre_save, sender=UserProfile)
def delete_old_profile_picture(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = UserProfile.objects.get(pk=instance.pk)
            old_pic = old_instance.profile_picture
            new_pic = instance.profile_picture

            if old_pic and old_pic != new_pic:
                if os.path.basename(old_pic.name) != 'def_prof.png':
                    print(f"Törlésre kerül: {old_pic.name}")
                    old_pic.delete(save=False)
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
