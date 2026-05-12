from django.core.mail import EmailMessage
from django.conf import settings

def send_reset_email(to_email, subject, html_content):
    try:
        email = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )
        email.content_subtype = "html"
        email.send(fail_silently=True)  # IMPORTANT CHANGE

    except Exception as e:
        print("EMAIL FAILED:", str(e))