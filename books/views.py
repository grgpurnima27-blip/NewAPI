from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import cloudinary.uploader
import resend
import logging

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
            "email":    openapi.Schema(type=openapi.TYPE_STRING),
            "password": openapi.Schema(type=openapi.TYPE_STRING),
        },
    )
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    username = request.data.get("username")
    email    = request.data.get("email")
    password = request.data.get("password")

    if not username or not email or not password:
        return Response({"error": "All fields required"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already taken"}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already registered"}, status=400)

    # Create user as INACTIVE until email is verified
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        is_active=False,
    )

    # Build verification link
    uid   = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    link  = f"{settings.BASE_URL}/api/verify-email/{uid}/{token}/"

    # Send verification email via Resend
    try:
        resend.Emails.send({
            "from":    settings.DEFAULT_FROM_EMAIL,
            "to":      [email],
            "subject": "Verify Your Email",
            "html": f"""
                <h2>Welcome, {username}!</h2>
                <p>Click the button below to verify your email and activate your account.</p>
                <br>
                <a href="{link}"
                   style="
                       padding: 10px 20px;
                       background: #16A34A;
                       color: white;
                       text-decoration: none;
                       border-radius: 5px;
                       font-weight: bold;
                   ">
                   Verify Email
                </a>
                <br><br>
                <p>If you did not create this account, ignore this email.</p>
                <p style="color: #999; font-size: 12px;">Link expires after first use.</p>
            """,
        })
        print(f"✅ Verification email sent to {email}")
    except Exception as e:
        # Roll back user creation if email fails so they can retry
        user.delete()
        logger.error(f"❌ Verification email failed: {e}")
        return Response(
            {"error": "Failed to send verification email. Please try again."},
            status=500
        )

    return Response(
        {"message": "Account created. Please check your email to verify your account."},
        status=201
    )


# VERIFY EMAIL 

@api_view(["GET"])
@permission_classes([AllowAny])
def verify_email(request, uidb64, token):
    try:
        uid  = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        return Response({"error": "Invalid verification link"}, status=400)

    if user.is_active:
        return Response({"message": "Email already verified. You can log in."})

    if not default_token_generator.check_token(user, token):
        return Response({"error": "Verification link is invalid or has expired."}, status=400)

    user.is_active = True
    user.save()

    return Response({"message": "Email verified successfully. You can now log in."})


# LOGIN 

@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["username", "password"],
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING),
            "password": openapi.Schema(type=openapi.TYPE_STRING),
        },
    )
)
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    # Give a clear message if user exists but is not verified
    try:
        user_obj = User.objects.get(username=username)
        if not user_obj.is_active:
            return Response(
                {"error": "Email not verified. Please check your inbox."},
                status=403
            )
    except User.DoesNotExist:
        pass

    user = authenticate(username=username, password=password)

    if not user:
        return Response({"error": "Invalid credentials"}, status=400)

    refresh = RefreshToken.for_user(user)

    return Response({
        "refresh": str(refresh),
        "access":  str(refresh.access_token),
    })


# LOGOUT 

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    return Response({"message": "Logged out successfully"})


# PROFILE — GET 

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)


#  PROFILE — UPDATE 

@swagger_auto_schema(
    method="patch",
    manual_parameters=[
        openapi.Parameter(
            "profile_picture",
            openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            description="Upload a new profile picture",
        ),
    ]
)
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def profile_update(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    image = request.FILES.get("profile_picture")
    if image:
        try:
            result = cloudinary.uploader.upload(
                image,
                folder="profile_pictures",
                public_id=f"avatar_{request.user.id}",
                overwrite=True,
                resource_type="image",
            )
            profile.profile_picture = result.get("public_id")
            profile.save()
        except Exception as e:
            logger.error(f"❌ Cloudinary upload failed: {e}")
            return Response({"error": "Image upload failed"}, status=500)

    serializer = ProfileSerializer(profile)
    return Response(serializer.data)


# RESET PASSWORD PAGE 

def reset_password_page(request, uidb64, token):
    return render(request, "reset_password.html", {
        "uidb64": uidb64,
        "token":  token,
    })


# VIEWSETS 

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by("-created_at")
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]