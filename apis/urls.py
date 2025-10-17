from django.urls import path
from apis.views import (
    # Auth views
    RegisterView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    LogoutView,
    ChangePasswordView,
    ForgotPasswordView,
    ResetPasswordView,
    CurrentUserView,
    # User views
    UserListCreateView,
    UserRetrieveUpdateDestroyView,
    ProfileListView,
    ProfileRetrieveUpdateDestroyView,
    UserSkillsListCreateView,
    UserSkillsRetrieveUpdateDestroyView,
    # Job views
    JobApplicationStatusListCreateView,
    JobApplicationStatusRetrieveUpdateDestroyView,
    JobSkillsListCreateView,
    JobSkillsRetrieveUpdateDestroyView,
    JobApplicationListCreateView,
    JobApplicationRetrieveUpdateDestroyView,
    # Learning views
    LearningManagementStatusListCreateView,
    LearningManagementStatusRetrieveUpdateDestroyView,
    LearningManagementListCreateView,
    LearningManagementRetrieveUpdateDestroyView,
    LearningResourceListCreateView,
    LearningResourceRetrieveUpdateDestroyView,
)

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('auth/forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('auth/reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('auth/me/', CurrentUserView.as_view(), name='current_user'),
    
    # User endpoints
    path('users/', UserListCreateView.as_view(), name='user_list_create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user_detail'),
    
    # Profile endpoints
    path('profiles/', ProfileListView.as_view(), name='profile_list'),
    path('profiles/<int:pk>/', ProfileRetrieveUpdateDestroyView.as_view(), name='profile_detail'),
    
    # User Skills endpoints
    path('user-skills/', UserSkillsListCreateView.as_view(), name='user_skills_list_create'),
    path('user-skills/<int:pk>/', UserSkillsRetrieveUpdateDestroyView.as_view(), name='user_skills_detail'),
    
    # Job Application Status endpoints
    path('job-statuses/', JobApplicationStatusListCreateView.as_view(), name='job_status_list_create'),
    path('job-statuses/<int:pk>/', JobApplicationStatusRetrieveUpdateDestroyView.as_view(), name='job_status_detail'),
    
    # Job Skills endpoints
    path('job-skills/', JobSkillsListCreateView.as_view(), name='job_skills_list_create'),
    path('job-skills/<int:pk>/', JobSkillsRetrieveUpdateDestroyView.as_view(), name='job_skills_detail'),
    
    # Job Application endpoints
    path('job-applications/', JobApplicationListCreateView.as_view(), name='job_application_list_create'),
    path('job-applications/<int:pk>/', JobApplicationRetrieveUpdateDestroyView.as_view(), name='job_application_detail'),
    
    # Learning Management Status endpoints
    path('learning-statuses/', LearningManagementStatusListCreateView.as_view(), name='learning_status_list_create'),
    path('learning-statuses/<int:pk>/', LearningManagementStatusRetrieveUpdateDestroyView.as_view(), name='learning_status_detail'),
    
    # Learning Management endpoints
    path('learning-plans/', LearningManagementListCreateView.as_view(), name='learning_plan_list_create'),
    path('learning-plans/<int:pk>/', LearningManagementRetrieveUpdateDestroyView.as_view(), name='learning_plan_detail'),
    
    # Learning Resource endpoints
    path('learning-resources/', LearningResourceListCreateView.as_view(), name='learning_resource_list_create'),
    path('learning-resources/<int:pk>/', LearningResourceRetrieveUpdateDestroyView.as_view(), name='learning_resource_detail'),
]