from rest_framework.response import Response
from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema, extend_schema_view
from apis.models import CustomUser, Profile, UserSkills, NotificationPreference, UserEmailSetting
from apis.serializers import (
    UserSerializer,
    UserCreateSerializer,
    ProfileSerializer,
    UserSkillsSerializer,
    UserUpdateSerializer,
    NotificationPreferenceSerializer,
    UpdateUserResumeSerializer,
    UserEmailSettingSerializer
)
from apis.utils.common import ServiceError


@extend_schema_view(
    get=extend_schema(
        summary="List all users",
        description="Retrieve a list of all users. Admin only.",
        tags=["Users"]
    ),
    post=extend_schema(
        summary="Create a new user",
        description="Create a new user account. Admin only.",
        tags=["Users"]
    )
)
class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAdminUser]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve user details",
        description="Get details of a specific user",
        tags=["Users"]
    ),
    put=extend_schema(
        summary="Update user",
        description="Update user information",
        tags=["Users"]
    ),
    patch=extend_schema(
        summary="Partially update user",
        description="Partially update user information",
        tags=["Users"]
    ),
    delete=extend_schema(
        summary="Delete user",
        description="Delete a user account. Admin only.",
        tags=["Users"]
    )
)
class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [permissions.IsAdminUser()]
        return super().get_permissions()
    
    def get_object(self):
        # Users can only access their own data unless they're admin
        obj = super().get_object()
        if not self.request.user.is_staff and obj != self.request.user:
            self.permission_denied(self.request, message="You can only access your own profile")
        return obj


@extend_schema_view(
    get=extend_schema(
        summary="Get current user profile",
        description="Retrieve the authenticated user's profile",
        tags=["Users"]
    )
)
class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


@extend_schema_view(
    get=extend_schema(
        summary="List user profiles",
        description="Retrieve a list of all user profiles",
        tags=["Profiles"]
    )
)
class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve profile",
        description="Get a specific user profile",
        tags=["Profiles"]
    ),
    put=extend_schema(
        summary="Update profile",
        description="Update user profile",
        tags=["Profiles"]
    ),
    patch=extend_schema(
        summary="Partially update profile",
        description="Partially update user profile",
        tags=["Profiles"]
    ),
    delete=extend_schema(
        summary="Delete profile",
        description="Delete a user profile",
        tags=["Profiles"]
    )
)
class ProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        obj = super().get_object()
        if not self.request.user.is_staff and obj.user != self.request.user:
            self.permission_denied(self.request, message="You can only access your own profile")
        return obj


@extend_schema_view(
    get=extend_schema(
        summary="List user skills",
        description="Retrieve a list of user skills",
        tags=["User Skills"]
    ),
    post=extend_schema(
        summary="Create user skill",
        description="Add a new skill to user profile",
        tags=["User Skills"]
    )
)
class UserSkillsListCreateView(generics.ListCreateAPIView):
    serializer_class = UserSkillsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own skills unless they're admin
        if self.request.user.is_staff:
            return UserSkills.objects.all()
        return UserSkills.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically set the user to the current user
        serializer.save(user=self.request.user)


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve user skill",
        description="Get details of a specific user skill",
        tags=["User Skills"]
    ),
    put=extend_schema(
        summary="Update user skill",
        description="Update a user skill",
        tags=["User Skills"]
    ),
    patch=extend_schema(
        summary="Partially update user skill",
        description="Partially update a user skill",
        tags=["User Skills"]
    ),
    delete=extend_schema(
        summary="Delete user skill",
        description="Remove a skill from user profile",
        tags=["User Skills"]
    )
)
class UserSkillsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSkillsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return UserSkills.objects.all()
        return UserSkills.objects.filter(user=self.request.user)



class UpdateUserProfileView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        if self.request.user.is_authenticated:
            return self.request.user
        raise ServiceError(error_message='User not authenticated', error_code=401)

    def perform_update(self, serializer):
        serializer.save()


class UpdateUserResumeView(generics.UpdateAPIView):
    serializer_class = UpdateUserResumeSerializer

    def get_object(self):
        if self.request.user.is_authenticated:
            return self.request.user
        raise ServiceError(error_message='User not authenticated', error_code=401)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        resume = request.FILES.get('resume')
        if resume:
            if hasattr(instance, 'profile'):
                instance.profile.resume = resume
            else:
                Profile.objects.create(user=instance, resume=resume)
        instance.save()
        return Response({'message': 'Resume updated successfully'}, status=200)

        

        

@extend_schema_view(
    get=extend_schema(
        summary="Get user notification preference",
        description="Retrieve the notification preference for the authenticated user",
        tags=["Notification Preference"]
    ),
    put=extend_schema(
        summary="Update user notification preference",
        description="Update the notification preference for the authenticated user",
        tags=["Notification Preference"]
    ),
    patch=extend_schema(
        summary="Partially update user notification preference",
        description="Partially update the notification preference for the authenticated user",
        tags=["Notification Preference"]
    )
)
class GetOrUpdateUserNotificationPreferenceView(generics.RetrieveUpdateAPIView):
    queryset = NotificationPreference.objects.all()
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'notification_preference'):
                return self.request.user.notification_preference
            return NotificationPreference.objects.create(user=self.request.user)
        raise ServiceError(error_message='User not authenticated', error_code=401)


@extend_schema_view(
    get=extend_schema(
        summary="List user email settings",
        description="Retrieve a list of email settings for the authenticated user",
        tags=["User Email Settings"]
    ),
    post=extend_schema(
        summary="Create user email setting",
        description="Add a new email setting for the authenticated user",
        tags=["User Email Settings"]
    )
)
class UserEmailSettingListCreateView(generics.ListCreateAPIView):
    serializer_class = UserEmailSettingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserEmailSetting.objects.filter(user=self.request.user)


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve user email setting",
        description="Get details of a specific email setting for the authenticated user",
        tags=["User Email Settings"]
    ),
    put=extend_schema(
        summary="Update user email setting",
        description="Update an email setting for the authenticated user",
        tags=["User Email Settings"]
    ),
    patch=extend_schema(
        summary="Partially update user email setting",
        description="Partially update an email setting for the authenticated user",
        tags=["User Email Settings"]
    ),
    delete=extend_schema(
        summary="Delete user email setting",
        description="Remove an email setting for the authenticated user",
        tags=["User Email Settings"]
    )
)
class UserEmailSettingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserEmailSettingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        email_setting_id = self.kwargs.get('pk')
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'user_email_settings'):
                if email_setting := self.request.user.user_email_settings.filter(id=email_setting_id).first():
                    return email_setting
            raise ServiceError(error_message='User email setting not found', error_code=404)
            
        raise ServiceError(error_message='User not authenticated', error_code=401)

    
    