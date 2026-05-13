import hashlib
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
import resend

# INIT RESEND

resend.api_key = settings.RESEND_API_KEY


# AVATAR GENERATOR (UNCHANGED)

AVATAR_COLORS = [
    "#E74C3C", "#8E44AD", "#2980B9", "#27AE60", "#F39C12",
    "#16A085", "#D35400", "#2C3E50", "#C0392B", "#1ABC9C",
]


def generate_avatar(user):
    first = (user.first_name[0] if user.first_name else user.username[0]).upper()
    last = (user.last_name[0] if user.last_name else "").upper()
    initials = f"{first}{last}" if last else first

    hash_int = int(hashlib.md5(user.username.encode()).hexdigest(), 16)
    color = AVATAR_COLORS[hash_int % len(AVATAR_COLORS)]

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

    filename = f"profile_pictures/{user.username}.svg"
    saved_path = default_storage.save(filename, ContentFile(svg.encode("utf-8")))
    return saved_path


# EMAIL SENDER (RESEND)


def send_reset_email(to_email, subject, message, html_content=None):
    try:
        params = {
            "from": "onboarding@resend.dev",
            "to": [to_email],
            "subject": subject,
            "html": html_content or f"<p>{message}</p>",
        }

        response = resend.Emails.send(params)

        print("✅ EMAIL SENT RESPONSE:", response)

    except Exception as e:
        print("❌ EMAIL FAILED:", str(e))
        raise e   # IMPORTANT: do NOT hide errors