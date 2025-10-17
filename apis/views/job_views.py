from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema, extend_schema_view
from apis.models import JobApplicationStatus, JobSkills, JobApplication
from apis.serializers import (
    JobApplicationStatusSerializer,
    JobSkillsSerializer,
    JobApplicationSerializer,
    JobApplicationCreateSerializer,
)


@extend_schema_view(
    get=extend_schema(
        summary="List job application statuses",
        description="Retrieve a list of all job application statuses",
        tags=["Job Management"]
    ),
    post=extend_schema(
        summary="Create job application status",
        description="Create a new job application status",
        tags=["Job Management"]
    )
)
class JobApplicationStatusListCreateView(generics.ListCreateAPIView):
    queryset = JobApplicationStatus.objects.all()
    serializer_class = JobApplicationStatusSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve job application status",
        description="Get details of a specific job application status",
        tags=["Job Management"]
    ),
    put=extend_schema(
        summary="Update job application status",
        description="Update a job application status",
        tags=["Job Management"]
    ),
    patch=extend_schema(
        summary="Partially update job application status",
        description="Partially update a job application status",
        tags=["Job Management"]
    ),
    delete=extend_schema(
        summary="Delete job application status",
        description="Delete a job application status",
        tags=["Job Management"]
    )
)
class JobApplicationStatusRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobApplicationStatus.objects.all()
    serializer_class = JobApplicationStatusSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(
    get=extend_schema(
        summary="List job skills",
        description="Retrieve a list of all job skills",
        tags=["Job Management"]
    ),
    post=extend_schema(
        summary="Create job skill",
        description="Create a new job skill",
        tags=["Job Management"]
    )
)
class JobSkillsListCreateView(generics.ListCreateAPIView):
    queryset = JobSkills.objects.all()
    serializer_class = JobSkillsSerializer
    permission_classes = [permissions.IsAdminUser]


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve job skill",
        description="Get details of a specific job skill",
        tags=["Job Management"]
    ),
    put=extend_schema(
        summary="Update job skill",
        description="Update a job skill",
        tags=["Job Management"]
    ),
    patch=extend_schema(
        summary="Partially update job skill",
        description="Partially update a job skill",
        tags=["Job Management"]
    ),
    delete=extend_schema(
        summary="Delete job skill",
        description="Delete a job skill",
        tags=["Job Management"]
    )
)
class JobSkillsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobSkills.objects.all()
    serializer_class = JobSkillsSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(
    get=extend_schema(
        summary="List job applications",
        description="Retrieve a list of job applications for the authenticated user",
        tags=["Job Applications"]
    ),
    post=extend_schema(
        summary="Create job application",
        description="Create a new job application",
        tags=["Job Applications"]
    )
)
class JobApplicationListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return JobApplicationCreateSerializer
        return JobApplicationSerializer
    
    def get_queryset(self):
        # Users can only see their own applications unless they're admin
        if self.request.user.is_staff:
            return JobApplication.objects.all()
        return JobApplication.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically set the user to the current user
        serializer.save(user=self.request.user)


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve job application",
        description="Get details of a specific job application",
        tags=["Job Applications"]
    ),
    put=extend_schema(
        summary="Update job application",
        description="Update a job application",
        tags=["Job Applications"]
    ),
    patch=extend_schema(
        summary="Partially update job application",
        description="Partially update a job application",
        tags=["Job Applications"]
    ),
    delete=extend_schema(
        summary="Delete job application",
        description="Delete a job application",
        tags=["Job Applications"]
    )
)
class JobApplicationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return JobApplication.objects.all()
        return JobApplication.objects.filter(user=self.request.user)
