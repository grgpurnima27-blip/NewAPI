import hashlib
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


#  AVATAR GENERATOR 

# 10 distinct pleasant colors, picked by hashing the username
AVATAR_COLORS = [
    "#E74C3C", "#8E44AD", "#2980B9", "#27AE60", "#F39C12",
    "#16A085", "#D35400", "#2C3E50", "#C0392B", "#1ABC9C",
]


def generate_avatar(user):
    """
    Generates an SVG initials avatar for the given user,
    saves it to media/profile_pictures/, and returns the relative path.
    """
    # --- Derive initials ---
    first = (user.first_name[0] if user.first_name else user.username[0]).upper()
    last  = (user.last_name[0]  if user.last_name  else "").upper()
    initials = f"{first}{last}" if last else first

    # --- Pick a stable color from username hash ---
    hash_int = int(hashlib.md5(user.username.encode()).hexdigest(), 16)
    color = AVATAR_COLORS[hash_int % len(AVATAR_COLORS)]

    # --- Build SVG ---
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="50" fill="{color}"/>
  <text x="50" y="50"
        font-family="Arial, sans-serif"
        font-size="{36 if len(initials) == 1 else 28}"
        font-weight="bold"
        fill="#FFFFFF"
        text-anchor="middle"
        dominant-baseline="central">
    {initials}
  </text>
</svg>"""

    # --- Save to media/profile_pictures/<username>.svg ---
    filename = f"profile_pictures/{user.username}.svg"
    saved_path = default_storage.save(filename, ContentFile(svg.encode("utf-8")))
    return saved_path


# EMAIL SENDER 

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings


def send_reset_email(to_email, subject, message, html_content=None):
    """
    Sends a password reset email via SMTP.
    Requires EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER,
    EMAIL_HOST_PASSWORD in Django settings.
    """
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = settings.EMAIL_HOST_USER
    msg["To"]      = to_email

    # Plain text fallback
    msg.attach(MIMEText(message, "plain"))

    # HTML version (if provided)
    if html_content:
        msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.EMAIL_HOST_USER, to_email, msg.as_string())