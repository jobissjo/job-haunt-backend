from .user_serializers import (
    UserSerializer,
    UserCreateSerializer,
    ProfileSerializer,
    UserSkillsSerializer,
    UserUpdateSerializer,
    NotificationPreferenceSerializer,
)

from .job_serializers import (
    JobApplicationStatusSerializer,
    JobSkillsSerializer,
    JobApplicationSerializer,
    JobApplicationCreateSerializer,
)
from .learning_serializers import (
    LearningManagementStatusSerializer,
    LearningManagementSerializer,
    LearningResourceSerializer,
    KanbanBoardLearningPlanSerializer,
    KanbanBoardLearningResourceSerializer,
)
from .auth_serializers import (
    RegisterSerializer,
    LoginSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    LogoutSerializer
)
from .common_serializers import MessageSerializer

__all__ = [
    'UserSerializer',
    'UserCreateSerializer',
    'ProfileSerializer',
    'UserSkillsSerializer',
    'UserUpdateSerializer',
    'JobApplicationStatusSerializer',
    'JobSkillsSerializer',
    'JobApplicationSerializer',
    'JobApplicationCreateSerializer',
    'LearningManagementStatusSerializer',
    'LearningManagementSerializer',
    'LearningResourceSerializer',
    'KanbanBoardLearningPlanSerializer',
    'KanbanBoardLearningResourceSerializer',
    'RegisterSerializer',
    'LoginSerializer',
    'CustomTokenObtainPairSerializer',
    'ChangePasswordSerializer',
    'ForgotPasswordSerializer',
    'ResetPasswordSerializer',
    'MessageSerializer',
    'LogoutSerializer',
    'NotificationPreferenceSerializer',
]
