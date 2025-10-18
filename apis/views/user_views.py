from nt import error
from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema, extend_schema_view
from apis.models import CustomUser, Profile, UserSkills, NotificationPreference
from apis.serializers import (
    UserSerializer,
    UserCreateSerializer,
    ProfileSerializer,
    UserSkillsSerializer,
    UserUpdateSerializer,
    NotificationPreferenceSerializer
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
    permission_classes = [permissions.IsAuthenticated]
    
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