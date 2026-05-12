from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from .utils import send_reset_email

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email = reset_password_token.user.email
    token = reset_password_token.key

    reset_link = f"https://newapi-jgbv.onrender.com/reset-password/{token}/"

    send_reset_email(
        to_email=email,
        subject="Reset Your Password",
        html_content=f"""
            <h2>Password Reset</h2>
            <p>Click below to reset your password:</p>
            <a href="{reset_link}">{reset_link}</a>
        """
    )