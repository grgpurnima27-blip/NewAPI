# books/signals.py
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from .utils import send_reset_email


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    print("🔥 SIGNAL TRIGGERED")  # ADD THIS

    send_reset_email(
        to_email=reset_password_token.user.email,
        subject="Password Reset",
        message=f"Token: {reset_password_token.key}",
        html_content=f"<p>Reset token: {reset_password_token.key}</p>"
    )