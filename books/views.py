from django.shortcuts import render
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Book, Category
from .serializers import BookSerializer, CategorySerializer, RegisterSerializer, LogoutSerializer

from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken


# SAFE EMAIL HELPER 

def send_email(to_email, subject, html_content):
    try:
        email = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )
        email.content_subtype = "html"
        email.send(fail_silently=True)   # IMPORTANT: prevents Render crash
    except Exception as e:
        print("Email error:", e)


# PAGINATION 

from rest_framework.pagination import PageNumberPagination

class BookPagination(PageNumberPagination):
    page_size = 5


# BOOK 

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = BookPagination


#CATEGORY 

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# REGISTER 

@swagger_auto_schema(
    method='post',
    request_body=RegisterSerializer,
    responses={
        201: openapi.Response(
            description="User registered successfully. Verification email sent."
        )
    }
)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    user = User.objects.create_user(
        username=serializer.validated_data['username'],
        password=serializer.validated_data['password'],
        email=serializer.validated_data['email'],
        is_active=False
    )

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    link = f"{settings.BASE_URL}/api/verify-email/{uid}/{token}/"

    send_email(
        user.email,
        "Verify Your Email",
        f"""
        <h2>Welcome!</h2>
        <p>Click below to verify your account:</p>
        <a href="{link}">{link}</a>
        """
    )

    return Response({"message": "Registration successful. Check email for verification"}, status=201)


# VERIFY EMAIL 

@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Email verified successfully. You can login."})

        return Response({"error": "Invalid token"}, status=400)

    except Exception:
        return Response({"error": "Invalid link"}, status=400)



# LOGOUT

@swagger_auto_schema(
    method='post',
    request_body=LogoutSerializer,
    responses={
        200: openapi.Response(description="Logged out successfully")
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):

    serializer = LogoutSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    try:
        refresh = serializer.validated_data["refresh"]

        token = RefreshToken(refresh)
        token.blacklist()

        return Response(
            {"message": "Logged out successfully"},
            status=200
        )

    except Exception:
        return Response(
            {"error": "Invalid token"},
            status=400
        )


# RESET PAGE 

def reset_password_page(request, token):
    return render(request, "reset_password.html", {"token": token})