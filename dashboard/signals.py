# dashboard/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import CustomUser
from .models import Profile

@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        # Update the profile if it exists
        if hasattr(instance, 'profile'):
            instance.profile.save()
        else:
            #If somehow profile is missing, create it
            Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()