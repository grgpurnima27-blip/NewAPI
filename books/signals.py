from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django_rest_passwordreset.signals import reset_password_token_created

from .models import Profile
from .utils import send_reset_email, generate_avatar


# ================= AUTO CREATE PROFILE =================

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        avatar_path = generate_avatar(instance)
        Profile.objects.create(user=instance, profile_picture=avatar_path)


# ================= PASSWORD RESET EMAIL =================

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    reset_link = f"https://newapi-jgbv.onrender.com/reset-password/{reset_password_token.key}/"

    send_reset_email(
        to_email=reset_password_token.user.email,
        subject="Password Reset Request",
        message=f"Click the link below to reset your password:\n{reset_link}",
        html_content=f"""
            <h2>Password Reset</h2>
            <p>Click the button below to reset your password:</p>
            <a href='{reset_link}'>Reset Password</a>
        """
    )