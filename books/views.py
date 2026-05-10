# from django.shortcuts import render
# from django.contrib.auth.models import User
# from django.conf import settings
# from django.core.mail import send_mail
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes
# from django.contrib.auth.tokens import default_token_generator

# from rest_framework import viewsets, status
# from rest_framework.permissions import (
#     IsAuthenticated,
#     AllowAny,
#     IsAuthenticatedOrReadOnly
# )
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.pagination import PageNumberPagination

# from drf_yasg.utils import swagger_auto_schema

# from .models import Book, Category
# from .serializers import *
# from .serializers import RegisterSerializer, LogoutSerializer


# # PAGINATION

# class BookPagination(PageNumberPagination):
#     page_size = 5
#     page_size_query_param = 'page_size'
#     max_page_size = 5


# # BOOK API

# class BookViewSet(viewsets.ModelViewSet):
#     queryset = Book.objects.all().order_by('-created_at')
#     serializer_class = BookSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     pagination_class = BookPagination


# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]


# # EMAIL VERIFICATION

# @api_view(['GET'])
# @permission_classes([AllowAny])
# def verify_email(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = User.objects.get(pk=uid)
#     except Exception:
#         return Response(
#             {'error': 'Invalid verification link'},
#             status=400
#         )

#     if default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()

#         return Response({
#             'message': 'Email verified successfully! You can now login.'
#         })

#     return Response(
#         {'error': 'Invalid or expired token'},
#         status=400
#     )


# # REGISTER USER

# @swagger_auto_schema(method='post', request_body=RegisterSerializer)
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register_view(request):
#     serializer = RegisterSerializer(data=request.data)

#     if not serializer.is_valid():
#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     username = serializer.validated_data.get('username')
#     password = serializer.validated_data.get('password')
#     email = serializer.validated_data.get('email', '')

#     if User.objects.filter(username=username).exists():
#         return Response(
#             {'error': 'Username already taken'},
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     user = User.objects.create_user(
#         username=username,
#         password=password,
#         email=email
#     )

#     # TEMPORARY: activate user directly
#     user.is_active = False
#     user.save()

#     # EMAIL VERIFICATION TEMPORARILY DISABLED
#     # Uncomment later after SMTP/email is configured correctly

    
#     uid = urlsafe_base64_encode(force_bytes(user.pk))
#     token = default_token_generator.make_token(user)

#     BASE_URL = getattr(settings, 'BASE_URL', 'http://127.0.0.1:8000')
#     verify_link = f"{BASE_URL}/api/verify-email/{uid}/{token}/"

#     send_mail(
#         subject="Verify your email",
#         message=f"Click to verify your account: {verify_link}",
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[email],
#         fail_silently=False
#     )
    

#     return Response({
#         'message': 'Account created successfully!'
#     }, status=status.HTTP_201_CREATED)


# # LOGOUT

# @swagger_auto_schema(method='post', request_body=LogoutSerializer)
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def logout_view(request):
#     try:
#         refresh_token = request.data.get('refresh')
#         token = RefreshToken(refresh_token)
#         token.blacklist()

#         return Response(
#             {'message': 'Logged out successfully!'},
#             status=status.HTTP_205_RESET_CONTENT
#         )

#     except Exception:
#         return Response(
#             {'error': 'Invalid or expired token'},
#             status=status.HTTP_400_BAD_REQUEST
#         )


# # RESET PASSWORD PAGE

# def reset_password_page(request, token):
#     return render(request, 'reset_password.html', {'token': token})

    
from django.shortcuts import render
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination

from drf_yasg.utils import swagger_auto_schema

from .models import Book, Category
from .serializers import BookSerializer, CategorySerializer, RegisterSerializer, LogoutSerializer



# PAGINATION


class BookPagination(PageNumberPagination):
    page_size = 5



# VIEWSETS (BOOK API)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = BookPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



# EMAIL VERIFICATION


@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Email verified successfully. You can now log in."})

        return Response({"error": "Invalid or expired token."}, status=400)

    except Exception:
        return Response({"error": "Invalid verification link."}, status=400)



# REGISTER


@swagger_auto_schema(method='post', request_body=RegisterSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']
    email = serializer.validated_data.get('email', '')

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists."}, status=400)

    if not email:
        return Response({"error": "Email is required."}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already registered."}, status=400)

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
    )
    user.is_active = False
    user.save()

    # Build verification link
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    BASE_URL = settings.BASE_URL
    verify_link = f"{BASE_URL}/api/verify-email/{uid}/{token}/"

    try:
        send_mail(
            subject="Verify your email - Book API",
            message=f"Hi {username},\n\nClick the link below to verify your email:\n\n{verify_link}\n\nIf you did not register, ignore this email.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception as e:
        # If email fails, delete the user so they can try again
        user.delete()
        return Response({"error": f"Failed to send verification email: {str(e)}"}, status=500)

    return Response({"message": "Registration successful. Please check your email to verify your account."}, status=201)



# LOGOUT (JWT BLACKLIST)


@swagger_auto_schema(method='post', request_body=LogoutSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh = request.data.get("refresh")
        if not refresh:
            return Response({"error": "Refresh token is required."}, status=400)

        token = RefreshToken(refresh)
        token.blacklist()

        return Response({"message": "Logged out successfully."}, status=205)

    except Exception:
        return Response({"error": "Invalid or expired token."}, status=400)



# PASSWORD RESET PAGE (HTML)

def reset_password_page(request, token):
    return render(request, 'reset_password.html', {'token': token})