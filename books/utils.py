from mailjet_rest import Client
from django.conf import settings


def send_reset_email(email, token):

    reset_link = f"{settings.BASE_URL}/reset-password/{token}/"

    mailjet = Client(
        auth=(
            settings.MAILJET_API_KEY,
            settings.MAILJET_API_SECRET
        ),
        version='v3.1'
    )

    data = {
        'Messages': [
            {
                "From": {
                    "Email": settings.MAILJET_SENDER_EMAIL,
                    "Name": settings.MAILJET_SENDER_NAME
                },
                "To": [
                    {
                        "Email": email,
                    }
                ],
                "Subject": "Password Reset",
                "HTMLPart": f"""
                    <p>Click below to reset your password:</p>
                    <p>
                        <a href="{reset_link}">
                            Reset Password
                        </a>
                    </p>
                """
            }
        ]
    }

    result = mailjet.send.create(data=data)

    print(result.status_code)
    print(result.json())

    return result.json()