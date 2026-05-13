from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from .models import Profile
from .utils import generate_avatar


# AUTO CREATE PROFILE 

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        avatar_path = generate_avatar(instance)
        Profile.objects.create(user=instance, profile_picture=avatar_path)