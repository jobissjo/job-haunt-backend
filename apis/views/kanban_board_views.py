from django.db.models.aggregates import Case, When, Value, IntegerField
from rest_framework.generics import ListAPIView
from apis.serializers import KanbanBoardLearningPlanSerializer, KanbanBoardLearningResourceSerializer
from apis.models import LearningManagementStatus
from drf_spectacular.utils import OpenApiParameter, extend_schema_view, extend_schema
from rest_framework.response import Response

@extend_schema_view(
    get=extend_schema(
        summary="Get Kanban Board Learning Plans",
        description="Get Kanban Board Learning Plans",
        tags=['KanbanBoard']
    )
)
class KanbanBoardLearningPlanView(ListAPIView):
    serializer_class = KanbanBoardLearningPlanSerializer
    
    def get_queryset(self):
        return LearningManagementStatus.objects.annotate(
            order=Case(
                When(category='start', then=Value(1)),
                When(category='in_progress', then=Value(2)),
                When(category='completed', then=Value(3)),
                output_field=IntegerField(),
            )
        ).prefetch_related('learning_managements').order_by('order')
    


@extend_schema_view(
    get=extend_schema(
        summary="Get Kanban Board Learning Resources",
        description="Get Kanban Board Learning Resources",
        tags=['KanbanBoard'],
        parameters=[
            OpenApiParameter(
                name='learning_management_id',
                description='Learning Management ID',
                required=False,
                type=int,
                location=OpenApiParameter.QUERY
            )
        ]
    )
)
class KanbanBoardLearningResourceView(ListAPIView):
    serializer_class = KanbanBoardLearningResourceSerializer
    
    def get_queryset(self):
        return LearningManagementStatus.objects.prefetch_related('learning_resources').annotate(
            order=Case(
                When(category='start', then=Value(1)),
                When(category='in_progress', then=Value(2)),
                When(category='completed', then=Value(3)),
                output_field=IntegerField(),
            )
        ).order_by('order')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        learning_management_id = request.query_params.get('learning_management_id')
        serializer = self.get_serializer(queryset, many=True, context={'request': request, 'learning_management_id': learning_management_id})
        return Response(serializer.data)