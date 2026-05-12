from django.core.mail import EmailMessage
from django.conf import settings

def send_reset_email(to_email, token):
    reset_link = f"{settings.BASE_URL}/reset-password/{token}/"

    email = EmailMessage(
        subject="Reset Password",
        body=f"Click here: {reset_link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )

    try:
        email.send(fail_silently=False)
    except Exception as e:
        print("EMAIL ERROR:", e)