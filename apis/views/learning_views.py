from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema, extend_schema_view
from apis.models import LearningManagementStatus, LearningManagement, LearningResource
from apis.serializers import (
    LearningManagementStatusSerializer,
    LearningManagementSerializer,
    LearningResourceSerializer,
)


@extend_schema_view(
    get=extend_schema(
        summary="List learning management statuses",
        description="Retrieve a list of learning management statuses for the authenticated user",
        tags=["Learning Management"]
    ),
    post=extend_schema(
        summary="Create learning management status",
        description="Create a new learning management status",
        tags=["Learning Management"]
    )
)
class LearningManagementStatusListCreateView(generics.ListCreateAPIView):
    serializer_class = LearningManagementStatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return LearningManagementStatus.objects.all()
        return LearningManagementStatus.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve learning management status",
        description="Get details of a specific learning management status",
        tags=["Learning Management"]
    ),
    put=extend_schema(
        summary="Update learning management status",
        description="Update a learning management status",
        tags=["Learning Management"]
    ),
    patch=extend_schema(
        summary="Partially update learning management status",
        description="Partially update a learning management status",
        tags=["Learning Management"]
    ),
    delete=extend_schema(
        summary="Delete learning management status",
        description="Delete a learning management status",
        tags=["Learning Management"]
    )
)
class LearningManagementStatusRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LearningManagementStatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return LearningManagementStatus.objects.all()
        return LearningManagementStatus.objects.filter(user=self.request.user)


@extend_schema_view(
    get=extend_schema(
        summary="List learning plans",
        description="Retrieve a list of learning plans for the authenticated user",
        tags=["Learning Management"]
    ),
    post=extend_schema(
        summary="Create learning plan",
        description="Create a new learning plan",
        tags=["Learning Management"]
    )
)
class LearningManagementListCreateView(generics.ListCreateAPIView):
    serializer_class = LearningManagementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return LearningManagement.objects.all()
        return LearningManagement.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve learning plan",
        description="Get details of a specific learning plan",
        tags=["Learning Management"]
    ),
    put=extend_schema(
        summary="Update learning plan",
        description="Update a learning plan",
        tags=["Learning Management"]
    ),
    patch=extend_schema(
        summary="Partially update learning plan",
        description="Partially update a learning plan",
        tags=["Learning Management"]
    ),
    delete=extend_schema(
        summary="Delete learning plan",
        description="Delete a learning plan",
        tags=["Learning Management"]
    )
)
class LearningManagementRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LearningManagementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return LearningManagement.objects.all()
        return LearningManagement.objects.filter(user=self.request.user)


@extend_schema_view(
    get=extend_schema(
        summary="List learning resources",
        description="Retrieve a list of learning resources",
        tags=["Learning Resources"]
    ),
    post=extend_schema(
        summary="Create learning resource",
        description="Create a new learning resource",
        tags=["Learning Resources"]
    )
)
class LearningResourceListCreateView(generics.ListCreateAPIView):
    queryset = LearningResource.objects.all()
    serializer_class = LearningResourceSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve learning resource",
        description="Get details of a specific learning resource",
        tags=["Learning Resources"]
    ),
    put=extend_schema(
        summary="Update learning resource",
        description="Update a learning resource",
        tags=["Learning Resources"]
    ),
    patch=extend_schema(
        summary="Partially update learning resource",
        description="Partially update a learning resource",
        tags=["Learning Resources"]
    ),
    delete=extend_schema(
        summary="Delete learning resource",
        description="Delete a learning resource",
        tags=["Learning Resources"]
    )
)
class LearningResourceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LearningResource.objects.all()
    serializer_class = LearningResourceSerializer
    permission_classes = [permissions.IsAuthenticated]
