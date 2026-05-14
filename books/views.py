# from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
# from django.shortcuts import render
# from django.conf import settings

# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_str
# from django.contrib.auth.tokens import default_token_generator

# from rest_framework.decorators import api_view, permission_classes, parser_classes
# from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework import viewsets

# import resend
# import logging

# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi

# from .models import Book, Category, Profile
# from .serializers import BookSerializer, CategorySerializer, ProfileSerializer

# logger = logging.getLogger(__name__)

# resend.api_key = settings.RESEND_API_KEY


# # REGISTER + EMAIL VERIFY

# @swagger_auto_schema(
#     method="post",
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         required=["username", "email", "password"],
#         properties={
#             "username": openapi.Schema(type=openapi.TYPE_STRING),
#             "email": openapi.Schema(type=openapi.TYPE_STRING),
#             "password": openapi.Schema(type=openapi.TYPE_STRING),
#         },
#     )
# )
# @api_view(["POST"])
# @permission_classes([AllowAny])
# def register_view(request):

#     username = request.data.get("username")
#     email = request.data.get("email")
#     password = request.data.get("password")

#     if not username or not email or not password:
#         return Response({"error": "All fields required"}, status=400)

#     if User.objects.filter(username=username).exists():
#         return Response({"error": "Username already exists"}, status=400)

#     if User.objects.filter(email=email).exists():
#         return Response({"error": "Email already exists"}, status=400)

#     # user inactive until email verified
#     user = User.objects.create_user(
#         username=username,
#         email=email,
#         password=password,
#         is_active=False
#     )

#     Profile.objects.get_or_create(user=user)

#     # create verification token
#     uid = urlsafe_base64_encode(force_bytes(user.pk))
#     token = default_token_generator.make_token(user)

#     verify_link = f"{settings.BASE_URL}/api/verify-email/{uid}/{token}/"

#     # IMPORTANT: do NOT crash register if email fails
#     try:
#         resend.Emails.send({
#             "from": settings.DEFAULT_FROM_EMAIL,
#             "to": [email],
#             "subject": "Verify Your Email",
#             "html": f"""
#                 <h2>Verify Your Account</h2>
#                 <p>Click below to activate your account:</p>
#                 <a href="{verify_link}">Verify Email</a>
#             """
#         })
#     except Exception as e:
#         logger.error(f"Email send failed: {str(e)}")

#     return Response({
#         "message": "User registered. Please check your email to verify account.",
#         # "verify_link_for_testing": verify_link  # remove in production
#     }, status=201)


# # VERIFY EMAIL

# @api_view(["GET"])
# @permission_classes([AllowAny])
# def verify_email(request, uidb64, token):

#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except:
#         return Response({"error": "Invalid link"}, status=400)

#     if not default_token_generator.check_token(user, token):
#         return Response({"error": "Invalid or expired token"}, status=400)

#     user.is_active = True
#     user.save()

#     return Response({"message": "Email verified successfully"})


# # LOGIN (BLOCK IF NOT VERIFIED)

# @api_view(["POST"])
# @permission_classes([AllowAny])
# def login_view(request):

#     username = request.data.get("username")
#     password = request.data.get("password")

#     user = authenticate(username=username, password=password)

#     if not user:
#         return Response({"error": "Invalid credentials"}, status=400)

#     if not user.is_active:
#         return Response({"error": "Email not verified"}, status=403)

#     refresh = RefreshToken.for_user(user)

#     return Response({
#         "refresh": str(refresh),
#         "access": str(refresh.access_token)
#     })


# # LOGOUT

# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def logout_view(request):
#     return Response({"message": "Logged out"})


# # FORGOT PASSWORD (EMAIL ONLY)

# @swagger_auto_schema(
#     method="post",
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         required=["email"],
#         properties={
#             "email": openapi.Schema(type=openapi.TYPE_STRING),
#         },
#     )
# )
# @api_view(["POST"])
# @permission_classes([AllowAny])
# def forgot_password(request):

#     email = request.data.get("email")

#     try:
#         user = User.objects.get(email=email)
#     except:
#         return Response({"error": "User not found"}, status=404)

#     uid = urlsafe_base64_encode(force_bytes(user.pk))
#     token = default_token_generator.make_token(user)

#     reset_link = f"{settings.BASE_URL}/api/reset-password/{uid}/{token}/"

#     try:
#         resend.Emails.send({
#             "from": settings.DEFAULT_FROM_EMAIL,
#             "to": [email],
#             "subject": "Reset Password",
#             "html": f"""
#                 <h2>Password Reset</h2>
#                 <a href="{reset_link}">Reset Password</a>
#             """
#         })
#     except Exception as e:
#         logger.error(f"Reset email failed: {str(e)}")

#     return Response({"message": "Reset email sent"})



# # RESET PAGE (HTML)

# def reset_password_page(request, uidb64, token):
#     return render(request, "reset_password.html", {
#         "uidb64": uidb64,
#         "token": token
#     })


# # RESET CONFIRM
# @swagger_auto_schema(
#     method="post",
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         required=["uidb64", "token", "password"],
#         properties={
#             "uidb64": openapi.Schema(type=openapi.TYPE_STRING),
#             "token": openapi.Schema(type=openapi.TYPE_STRING),
#             "password": openapi.Schema(type=openapi.TYPE_STRING),
#         },
#     )
# )

# @api_view(["POST"])
# @permission_classes([AllowAny])
# def password_reset_confirm(request):

#     uidb64 = request.data.get("uidb64")
#     token = request.data.get("token")
#     password = request.data.get("password")
#     if not uidb64 or not token or not password:
#         return Response({"error": "All fields required"}, status=400)

#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except:
#         return Response({"error": "Invalid link"}, status=400)

#     if not default_token_generator.check_token(user, token):
#         return Response({"error": "Token expired"}, status=400)

#     user.set_password(password)
#     user.save()

#     return Response({"message": "Password reset successful"})


# # PROFILE

# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def profile_view(request):

#     profile, _ = Profile.objects.get_or_create(user=request.user)
#     return Response(ProfileSerializer(profile).data)


# @api_view(["PATCH"])
# @permission_classes([IsAuthenticated])
# @parser_classes([MultiPartParser, FormParser])
# def profile_update(request):

#     profile, _ = Profile.objects.get_or_create(user=request.user)

#     image = request.FILES.get("profile_picture")

#     if image:
#         profile.profile_picture = image
#         profile.save()

#     return Response(ProfileSerializer(profile).data)


# # VIEWSETS

# class BookViewSet(viewsets.ModelViewSet):
#     queryset = Book.objects.all().order_by("-created_at")
#     serializer_class = BookSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]


# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from django.conf import settings

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets

import resend
import logging

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Book, Category, Profile
from .serializers import BookSerializer, CategorySerializer, ProfileSerializer

logger = logging.getLogger(__name__)
resend.api_key = settings.RESEND_API_KEY


# REGISTER

@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["username", "email", "password"],
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING),
            "email": openapi.Schema(type=openapi.TYPE_STRING),
            "password": openapi.Schema(type=openapi.TYPE_STRING),
        },
    )
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):

    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not email or not password:
        return Response({"error": "All fields required"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username exists"}, status=400)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        is_active=False
    )

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    verify_link = f"{settings.BASE_URL}/api/verify-email/{uid}/{token}/"

    # DO NOT BREAK API IF EMAIL FAILS
    try:
        resend.Emails.send({
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": [email],
            "subject": "Verify Email",
            "html": f"<a href='{verify_link}'>Verify Account</a>"
        })
    except Exception as e:
        logger.error(f"Email error: {str(e)}")

    return Response({"message": "User created. Check email."}, status=201)



# VERIFY EMAIL

@api_view(["GET"])
@permission_classes([AllowAny])
def verify_email(request, uidb64, token):

    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)

    if not default_token_generator.check_token(user, token):
        return Response({"error": "Invalid token"}, status=400)

    user.is_active = True
    user.save()

    return Response({"message": "Email verified"})


# LOGIN

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):

    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if not user:
        return Response({"error": "Invalid credentials"}, status=400)

    if not user.is_active:
        return Response({"error": "Verify email first"}, status=403)

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    })



# FORGOT PASSWORD

@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["email"],
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING),
        },
    )
)
@api_view(["POST"])
@permission_classes([AllowAny])
def forgot_password(request):

    email = request.data.get("email")

    user = User.objects.filter(email=email).first()

    if not user:
        return Response({"error": "User not found"}, status=404)

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    reset_link = f"{settings.BASE_URL}/reset-password/{uid}/{token}/"

    try:
        resend.Emails.send({
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": [email],
            "subject": "Reset Password",
            "html": f"<a href='{reset_link}'>Reset Password</a>"
        })
    except Exception as e:
        logger.error(str(e))

    return Response({"message": "Reset email sent"})


# RESET PAGE (HTML)

def reset_password_page(request, uidb64, token):
    return render(request, "reset_password.html", {
        "uidb64": uidb64,
        "token": token
    })


# RESET CONFIRM

@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["uidb64", "token", "password"],
        properties={
            "uidb64": openapi.Schema(type=openapi.TYPE_STRING),
            "token": openapi.Schema(type=openapi.TYPE_STRING),
            "password": openapi.Schema(type=openapi.TYPE_STRING),
        },
    )
)

@api_view(["POST"])
@permission_classes([AllowAny])
def password_reset_confirm(request):

    uidb64 = request.data.get("uidb64")
    token = request.data.get("token")
    password = request.data.get("password")

    if not password:
        return Response({"error": "Password required"}, status=400)

    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)

    if not default_token_generator.check_token(user, token):
        return Response({"error": "Invalid token"}, status=400)

    user.set_password(password)
    user.save()

    return Response({"message": "Password reset successful"})


# PROFILE

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return Response(ProfileSerializer(profile).data)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def profile_update(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    image = request.FILES.get("profile_picture")

    if image:
        profile.profile_picture = image
        profile.save()

    return Response(ProfileSerializer(profile).data)


# VIEWSETS

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by("-created_at")
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]