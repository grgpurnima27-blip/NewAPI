from django.shortcuts import render
from django.contrib.auth.models import User
from django.conf import settings
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
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
 
import resend
 
 
# HELPER: Send email via Resend
 
def send_resend_email(to_email, subject, html_content):
    resend.api_key = settings.RESEND_API_KEY
    resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": to_email,
        "subject": subject,
        "html": html_content,
    })
 
 
# PAGINATION
 
class BookPagination(PageNumberPagination):
    page_size = 5
 
 
# VIEWSETS
 
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
 
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    verify_link = f"{settings.BASE_URL}/api/verify-email/{uid}/{token}/"
 
    try:
        send_resend_email(
            to_email=email,
            subject="Verify your email - Book API",
            html_content="<h2>Hi " + username + ",</h2><p>Click the link below to verify your email:</p><p><a href='" + verify_link + "'>" + verify_link + "</a></p><p>If you did not register, ignore this email.</p>"
        )
    except Exception as e:
        user.delete()
        return Response({"error": f"Failed to send verification email: {str(e)}"}, status=500)
 
    return Response({"message": "Registration successful. Please check your email to verify your account."}, status=201)
 
 
# TEST EMAIL
 
@api_view(['POST'])
@permission_classes([AllowAny])
def test_email(request):
    results = {}
    try:
        send_resend_email(
            to_email=request.data.get('email'),
            subject='Test Email from Django',
            html_content='<p>If you receive this, email is working!</p>'
        )
        results['email_sent'] = True
        results['email_error'] = None
    except Exception as e:
        results['email_sent'] = False
        results['email_error'] = str(e)
 
    return Response(results)
 
 
# PASSWORD RESET
 
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    reset_link = f"{settings.BASE_URL}/reset-password/{reset_password_token.key}/"
 
    try:
        send_resend_email(
            to_email=reset_password_token.user.email,
            subject="Reset your password - Book API",
            html_content="<h2>Password Reset</h2><p>Click the link below to reset your password:</p><p><a href='" + reset_link + "'>" + reset_link + "</a></p><p>If you did not request this, ignore this email.</p>"
        )
    except Exception as e:
        print(f"[PASSWORD RESET] Email failed: {e}")
 
 
# LOGOUT
 
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
 
 
# PASSWORD RESET PAGE
 
def reset_password_page(request, token):
    return render(request, 'reset_password.html', {'token': token})