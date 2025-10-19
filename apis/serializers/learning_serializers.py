from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from apis.models.learning_managment import LearningManagementStatus, LearningManagement, LearningResource


class LearningManagementStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningManagementStatus
        fields = ['id', 'name', 'category', 'color', 'user']
        read_only_fields = ['id', 'user']
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        else:
            raise serializers.ValidationError("User is not authenticated")
        return super().create(validated_data)


class LearningResourceSerializer(serializers.ModelSerializer):
    status_detail = LearningManagementStatusSerializer(source='status', read_only=True)
    
    class Meta:
        model = LearningResource
        fields = [
            'id', 'name', 'resource_type', 'resource_url', 'learning_management',
            'status', 'status_detail', 'expected_started_date', 'expected_completed_date',
            'actual_started_date', 'actual_completed_date', 'description',
            'completed_percentage', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LearningManagementSerializer(serializers.ModelSerializer):
    status_detail = LearningManagementStatusSerializer(source='status', read_only=True)
    resources = LearningResourceSerializer(source='learningresource_set', many=True, read_only=True)
    
    class Meta:
        model = LearningManagement
        fields = [
            'id', 'name', 'description', 'expected_started_date',
            'expected_completed_date', 'actual_started_date',
            'actual_completed_date', 'status', 'status_detail',
            'completed_percentage',  'resources',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        else:
            raise serializers.ValidationError("User is not authenticated")
        return super().create(validated_data)


class KanbanBoardLearningPlanSerializer(serializers.ModelSerializer):
    learning_managements = serializers.SerializerMethodField()
    class Meta:
        model = LearningManagementStatus
        fields = '__all__'

    @extend_schema_field(LearningManagementSerializer(many=True))
    def get_learning_managements(self, obj):
        return LearningManagementSerializer(obj.learning_managements.order_by('-created_at'), many=True).data


class KanbanBoardLearningResourceSerializer(serializers.ModelSerializer):
    learning_resources = serializers.SerializerMethodField()
    class Meta:
        model = LearningManagementStatus
        fields = '__all__'
    
    @extend_schema_field(LearningResourceSerializer(many=True))
    def get_learning_resources(self, obj):
        learning_management_id = self.context.get('learning_management_id')
        if learning_management_id:
            learning_resources = obj.learning_resources.filter(learning_management_id=learning_management_id).order_by('-created_at')
        else:
            learning_resources = obj.learning_resources.order_by('-created_at')
        return LearningResourceSerializer(learning_resources, many=True).data