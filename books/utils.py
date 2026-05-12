from django.core.mail import EmailMessage
from django.conf import settings

def send_reset_email(to_email, token, html_content=None):

    reset_link = f"{settings.BASE_URL}/reset-password/{token}/"

    if html_content is None:
        html_content = f"""
        <h2>Password Reset</h2>
        <p>Click below to reset password:</p>
        <a href="{reset_link}">{reset_link}</a>
        """

    email = EmailMessage(
        subject="Reset Your Password",
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )
    email.content_subtype = "html"
    email.send(fail_silently=False)