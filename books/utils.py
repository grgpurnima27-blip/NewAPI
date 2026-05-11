import resend
from django.conf import settings

def send_reset_email(email, token):
    reset_link = f"{settings.BASE_URL}/reset-password/{token}/"
    
    resend.api_key = settings.RESEND_API_KEY
    resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": email,
        "subject": "Password Reset",
        "html": f"<p>Click here to reset your password: <a href='{reset_link}'>{reset_link}</a></p>"
    })