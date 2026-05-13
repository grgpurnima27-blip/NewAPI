from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.conf import settings

import resend
import logging

logger = logging.getLogger(__name__)

# SAFE INIT (won't crash if env missing)
resend.api_key = getattr(settings, "RESEND_API_KEY", None)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    try:
        reset_link = f"{settings.BASE_URL}/reset-password/{reset_password_token.key}/"

        resend.Emails.send({
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": [reset_password_token.user.email],
            "subject": "Reset Your Password",
            "html": f"""
                <h2>Password Reset</h2>
                <p>Click below to reset your password:</p>
                <a href="{reset_link}">Reset Password</a>
            """
        })

        print("🔥 Password reset email sent")

    except Exception as e:
        # ❗ NEVER crash Render because of email failure
        logger.error(f"Email sending failed: {e}")
        print("❌ Email failed but app continues running")