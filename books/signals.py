import hashlib
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.conf import settings

from django_rest_passwordreset.signals import reset_password_token_created

import cloudinary.uploader
import resend

from .models import Profile

logger = logging.getLogger(__name__)

resend.api_key = getattr(settings, "RESEND_API_KEY", None)


# AVATAR 

AVATAR_COLORS = [
    "#E74C3C", "#8E44AD", "#2980B9", "#27AE60",
    "#F39C12", "#16A085", "#D35400", "#2C3E50",
    "#C0392B", "#1ABC9C",
]


def generate_and_upload_avatar(user):
    first    = (user.first_name[0] if user.first_name else user.email[0] if user.email else user.username[0]).upper()
    last     = (user.last_name[0] if user.last_name else "").upper()
    initials = f"{first}{last}" if last else first

    seed     = user.email or user.username
    hash_int = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    color    = AVATAR_COLORS[hash_int % len(AVATAR_COLORS)]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
  <circle cx="50" cy="50" r="50" fill="{color}"/>
  <text x="50" y="50"
        font-size="{36 if len(initials) == 1 else 28}"
        text-anchor="middle"
        dominant-baseline="middle"
        fill="white">
    {initials}
  </text>
</svg>"""

    try:
        result = cloudinary.uploader.upload(
            ContentFile(svg.encode("utf-8"), name=f"{user.username}.svg"),
            folder="profile_pictures",
            public_id=f"avatar_{user.id}",
            resource_type="raw",  # SVG must be uploaded as raw
            overwrite=True,
        )
        return result.get("public_id")
    except Exception as e:
        logger.error(f"❌ Avatar upload failed for {user.username}: {e}")
        return None


# AUTO-CREATE PROFILE ON REGISTER 

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)

        public_id = generate_and_upload_avatar(instance)
        if public_id:
            profile.profile_picture = public_id
            profile.save()
            print(f"✅ Profile + avatar created for {instance.username}")
        else:
            print(f"⚠️ Profile created for {instance.username} but avatar upload failed")


#  PASSWORD RESET EMAIL 

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    try:
        reset_link =reset_link = f"{settings.BASE_URL}/api/reset-password/{reset_password_token.key}/"

        resend.Emails.send({
            "from":    settings.DEFAULT_FROM_EMAIL,
            "to":      [reset_password_token.user.email],
            "subject": "Reset Your Password",
            "html": f"""
                <h2>Password Reset</h2>
                <p>Click below to reset your password:</p>
                <br>
                <a href="{reset_link}"
                   style="
                       padding: 10px 20px;
                       background: #4F46E5;
                       color: white;
                       text-decoration: none;
                       border-radius: 5px;
                       font-weight: bold;
                   ">
                   Reset Password
                </a>
                <br><br>
                <p>If you didn't request this, ignore this email.</p>
            """,
        })
        print("🔥 Password reset email sent")

    except Exception as e:
        logger.error(f"❌ Email sending failed: {e}")
        print("❌ Email failed but app continues running")