from django.core.mail import send_mail

def send_reset_email(email, token):
    reset_link = f"http://127.0.0.1:8000/reset-password/{token}/"

    send_mail(
        "Password Reset",
        f"Click here to reset your password: {reset_link}",
        "grgpurnima27@gmail.com",
        [email],
        fail_silently=False,
    )