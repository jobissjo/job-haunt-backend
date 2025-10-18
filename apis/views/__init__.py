from .auth_views import (
    RegisterView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    LogoutView,
    ChangePasswordView,
    ForgotPasswordView,
    ResetPasswordView,
    CurrentUserView,
)
from .user_views import (
    UserListCreateView,
    UserRetrieveUpdateDestroyView,
    ProfileListView,
    ProfileRetrieveUpdateDestroyView,
    UserSkillsListCreateView,
    UserSkillsRetrieveUpdateDestroyView,
    UpdateUserProfileView,
    GetOrUpdateUserNotificationPreferenceView,
)
from .job_views import (
    JobApplicationStatusListCreateView,
    JobApplicationStatusRetrieveUpdateDestroyView,
    JobSkillsListCreateView,
    JobSkillsRetrieveUpdateDestroyView,
    JobApplicationListCreateView,
    JobApplicationRetrieveUpdateDestroyView,
)
from .learning_views import (
    LearningManagementStatusListCreateView,
    LearningManagementStatusRetrieveUpdateDestroyView,
    LearningManagementListCreateView,
    LearningManagementRetrieveUpdateDestroyView,
    LearningResourceListCreateView,
    LearningResourceRetrieveUpdateDestroyView,
)

__all__ = [
    # Auth views
    'RegisterView',
    'CustomTokenObtainPairView',
    'CustomTokenRefreshView',
    'LogoutView',
    'ChangePasswordView',
    'ForgotPasswordView',
    'ResetPasswordView',
    'CurrentUserView',
    # User views
    'UserListCreateView',
    'UserRetrieveUpdateDestroyView',
    'ProfileListView',
    'ProfileRetrieveUpdateDestroyView',
    'UserSkillsListCreateView',
    'UserSkillsRetrieveUpdateDestroyView',
    'UpdateUserProfileView',
    'GetOrUpdateUserNotificationPreferenceView',
    # Job views
    'JobApplicationStatusListCreateView',
    'JobApplicationStatusRetrieveUpdateDestroyView',
    'JobSkillsListCreateView',
    'JobSkillsRetrieveUpdateDestroyView',
    'JobApplicationListCreateView',
    'JobApplicationRetrieveUpdateDestroyView',
    # Learning views
    'LearningManagementStatusListCreateView',
    'LearningManagementStatusRetrieveUpdateDestroyView',
    'LearningManagementListCreateView',
    'LearningManagementRetrieveUpdateDestroyView',
    'LearningResourceListCreateView',
    'LearningResourceRetrieveUpdateDestroyView',
]
