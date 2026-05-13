import hashlib
import smtplib

from django.conf import settings

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.files.base import ContentFile

from cloudinary.uploader import upload


# AVATAR GENERATOR 

AVATAR_COLORS = [
    "#E74C3C",
    "#8E44AD",
    "#2980B9",
    "#27AE60",
    "#F39C12",
    "#16A085",
    "#D35400",
    "#2C3E50",
    "#C0392B",
    "#1ABC9C",
]


def generate_avatar(user):

    first = (
        user.first_name[0]
        if user.first_name
        else user.username[0]
    ).upper()

    last = (
        user.last_name[0]
        if user.last_name
        else ""
    ).upper()

    initials = f"{first}{last}" if last else first

    hash_int = int(
        hashlib.md5(user.username.encode()).hexdigest(),
        16
    )

    color = AVATAR_COLORS[hash_int % len(AVATAR_COLORS)]

    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
    <circle cx="50" cy="50" r="50" fill="{color}"/>
    <text
        x="50%"
        y="50%"
        dominant-baseline="middle"
        text-anchor="middle"
        font-size="36"
        fill="white"
        font-family="Arial"
    >
        {initials}
    </text>
</svg>
"""

    result = upload(
        ContentFile(svg.encode("utf-8")),
        folder="profile_pictures",
        public_id=user.username,
        resource_type="image",
        format="svg"
    )

    return result["public_id"]


# EMAIL SENDER 

def send_reset_email(
    to_email,
    subject,
    message,
    html_content=None
):

    msg = MIMEMultipart("alternative")

    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_HOST_USER
    msg["To"] = to_email

    msg.attach(MIMEText(message, "plain"))

    if html_content:
        msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(
        settings.EMAIL_HOST,
        settings.EMAIL_PORT
    ) as server:

        server.starttls()

        server.login(
            settings.EMAIL_HOST_USER,
            settings.EMAIL_HOST_PASSWORD
        )

        server.sendmail(
            settings.EMAIL_HOST_USER,
            to_email,
            msg.as_string()
        )