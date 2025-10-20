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
    UpdateUserResumeView,
    UserEmailSettingListCreateView,
    UserEmailSettingRetrieveUpdateDestroyView,
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
from .kanban_board_views import (
    KanbanBoardLearningPlanView,
    KanbanBoardLearningResourceView,
)
from .admin_views import (
    AdminStatsView,
    ExportAllTablesView,
    ImportJSONView,
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
    'UpdateUserResumeView',
    'UserEmailSettingListCreateView',
    'UserEmailSettingRetrieveUpdateDestroyView',
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
    # Kanbanboard Views
    'KanbanBoardLearningPlanView',
    'KanbanBoardLearningResourceView',
    # Admin views
    'AdminStatsView',
    'ExportAllTablesView',
    'ImportJSONView',    
]
