# import hashlib

# from django.conf import settings
# from django.core.files.base import ContentFile
# from django.core.files.storage import default_storage

# import resend


# # RESEND CONFIG

# resend.api_key = settings.RESEND_API_KEY



# # AVATAR COLORS

# AVATAR_COLORS = [
#     "#E74C3C",
#     "#8E44AD",
#     "#2980B9",
#     "#27AE60",
#     "#F39C12",
#     "#16A085",
#     "#D35400",
#     "#2C3E50",
#     "#C0392B",
#     "#1ABC9C",
# ]



# # GENERATE AVATAR

# def generate_avatar(user):

#     first = (
#         user.first_name[0]
#         if user.first_name
#         else user.email[0]
#     ).upper()

#     last = (
#         user.last_name[0]
#         if user.last_name
#         else ""
#     ).upper()

#     initials = f"{first}{last}" if last else first

#     hash_int = int(
#         hashlib.md5(user.email.encode()).hexdigest(),
#         16
#     )

#     color = AVATAR_COLORS[
#         hash_int % len(AVATAR_COLORS)
#     ]

#     svg = f"""
#     <svg xmlns="http://www.w3.org/2000/svg"
#          width="100"
#          height="100">

#       <circle
#         cx="50"
#         cy="50"
#         r="50"
#         fill="{color}"
#       />

#       <text
#         x="50"
#         y="50"
#         font-size="{36 if len(initials) == 1 else 28}"
#         text-anchor="middle"
#         dominant-baseline="middle"
#         fill="white">

#         {initials}

#       </text>

#     </svg>
#     """

#     filename = f"profile_pictures/{user.email}.svg"

#     return default_storage.save(
#         filename,
#         ContentFile(svg.encode("utf-8"))
#     )



# # SEND EMAIL VERIFICATION

# def send_verification_email(user, token):

#     verify_link = (
#         f"{settings.BASE_URL}"
#         f"/verify-email/{token}/"
#     )

#     try:

#         response = resend.Emails.send({

#             "from": settings.DEFAULT_FROM_EMAIL,

#             "to": [user.email],

#             "subject": "Verify Your Email",

#             "html": f"""
#                 <h2>Email Verification</h2>

#                 <p>
#                     Click below to verify your account:
#                 </p>

#                 <br>

#                 <a href="{verify_link}"
#                    style="
#                         padding:10px 15px;
#                         background:#16A34A;
#                         color:white;
#                         text-decoration:none;
#                         border-radius:5px;
#                    ">
#                    Verify Email
#                 </a>

#                 <br><br>

#                 <p>
#                     If you did not create this account,
#                     ignore this email.
#                 </p>
#             """
#         })

#         print("✅ VERIFICATION EMAIL SENT:", response)

#     except Exception as e:

#         print("❌ VERIFICATION EMAIL ERROR:", str(e))



# # SEND PASSWORD RESET EMAIL

# def send_reset_email(to_email, token):

#     reset_link = (
#         f"{settings.BASE_URL}"
#         f"/reset-password/{token}/"
#     )

#     try:

#         response = resend.Emails.send({

#             "from": settings.DEFAULT_FROM_EMAIL,

#             "to": [to_email],

#             "subject": "Password Reset Request",

#             "html": f"""
#                 <h2>Password Reset</h2>

#                 <p>
#                     Click below to reset your password:
#                 </p>

#                 <br>

#                 <a href="{reset_link}"
#                    style="
#                         padding:10px 15px;
#                         background:#4F46E5;
#                         color:white;
#                         text-decoration:none;
#                         border-radius:5px;
#                    ">
#                    Reset Password
#                 </a>

#                 <br><br>

#                 <p>
#                     If you didn't request this,
#                     ignore this email.
#                 </p>
#             """
#         })

#         print("🔥 PASSWORD RESET EMAIL SENT:", response)

#     except Exception as e:

#         print("❌ PASSWORD RESET EMAIL ERROR:", str(e))