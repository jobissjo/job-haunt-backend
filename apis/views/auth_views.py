from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from apis.models import CustomUser, PasswordResetToken
from apis.serializers import (
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    UserSerializer,
    MessageSerializer
)
from apis.services.email_service import EmailService


@extend_schema(
    summary="Register a new user",
    description="Create a new user account",
    tags=["Authentication"],
    request=RegisterSerializer,
    responses={201: UserSerializer}
)
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        refresh['role'] = user.role
        refresh['email'] = user.email
        refresh['username'] = user.username
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


@extend_schema(
    summary="Login",
    description="Authenticate user and get JWT tokens with role in claims",
    tags=["Authentication"],
    request=CustomTokenObtainPairSerializer,
    responses={200: CustomTokenObtainPairSerializer}
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(
    summary="Refresh token",
    description="Get a new access token using refresh token. Role is included in the new access token.",
    tags=["Authentication"]
)
class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom refresh view that ensures role is included in the refreshed access token
    """
    pass


@extend_schema(
    summary="Logout",
    description="Blacklist the refresh token to logout user",
    tags=["Authentication"],
    request=None,
    responses={200: MessageSerializer}
)
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response(
                {"message": "Successfully logged out"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(
    summary="Change password",
    description="Change password for authenticated user",
    tags=["Authentication"],
    request=ChangePasswordSerializer,
    responses={200: MessageSerializer}
)
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response(
                {"message": "Password changed successfully"},
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Forgot password",
    description="Request a password reset token. An email will be sent to the user with reset instructions.",
    tags=["Authentication"],
    request=ForgotPasswordSerializer,
    responses={200: MessageSerializer}
)
class ForgotPasswordView(APIView):

    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                user = CustomUser.objects.get(email=email)
                
                # Create password reset token
                reset_token = PasswordResetToken.objects.create(user=user)
                
                # Send email with reset token
                try:
                    EmailService.send_email_with_template(
                        template_name='password_reset.html',
                        context={
                            'user': user,
                            'reset_token': reset_token.token,
                            'reset_url': f"{request.scheme}://{request.get_host()}/api/auth/reset-password/?token={reset_token.token}"
                        },
                        subject='Password Reset Request',
                        to_emails=[user.email]
                    )
                except Exception as e:
                    # Log error but don't reveal to user
                    print(f"Email send error: {e}")
                
            except CustomUser.DoesNotExist:
                # Don't reveal if email exists or not for security
                pass
            
            # Always return success to prevent email enumeration
            return Response(
                {"message": "If the email exists, a password reset link has been sent"},
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Reset password",
    description="Reset password using the token received via email",
    tags=["Authentication"],
    request=ResetPasswordSerializer,
    responses={200: MessageSerializer}
)
class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            token_string = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            
            try:
                reset_token = PasswordResetToken.objects.get(token=token_string)
                
                if not reset_token.is_valid():
                    return Response(
                        {"error": "Token is invalid or has expired"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Reset password
                user = reset_token.user
                user.set_password(new_password)
                user.save()
                
                # Mark token as used
                reset_token.is_used = True
                reset_token.save()
                
                return Response(
                    {"message": "Password has been reset successfully"},
                    status=status.HTTP_200_OK
                )
                
            except PasswordResetToken.DoesNotExist:
                return Response(
                    {"error": "Invalid token"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Get current user",
    description="Get the currently authenticated user's information",
    tags=["Authentication"]
)
class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
