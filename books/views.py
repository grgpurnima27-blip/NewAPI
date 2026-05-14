from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Book, Category
from .serializers import BookSerializer, CategorySerializer
from .utils import send_verification_email


# REGISTER

@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):

    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not email or not password:
        return Response({"error": "All fields required"}, status=400)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        is_active=False
    )

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    send_verification_email(user, uid, token)

    return Response({"message": "Check email to verify account"}, status=201)


# VERIFY EMAIL

@api_view(["GET"])
@permission_classes([AllowAny])
def verify_email(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Email verified successfully"})

        return Response({"error": "Invalid token"}, status=400)

    except Exception:
        return Response({"error": "Invalid link"}, status=400)



# LOGIN (BLOCK INACTIVE USERS)

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):

    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if not user:
        return Response({"error": "Invalid credentials"}, status=400)

    if not user.is_active:
        return Response({"error": "Email not verified"}, status=403)

    refresh = RefreshToken.for_user(user)

    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    })


# LOGOUT

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    return Response({"message": "Logged out"})


# RESET PASSWORD

@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["email"],
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING)
        },
    ),
    responses={200: "Password reset email sent"}
)
@api_view(["POST"])
@permission_classes([AllowAny])
def password_reset_docs(request):
    return Response({"message": "Password reset handled by backend"})


def reset_password_page(request, token):
    return render(request, "reset_password.html", {"token": token})


# VIEWSETS

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by("-created_at")
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]