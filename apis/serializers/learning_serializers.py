from rest_framework import serializers
from apis.models.learning_managment import LearningManagementStatus, LearningManagement, LearningResource


class LearningManagementStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningManagementStatus
        fields = ['id', 'name', 'category', 'color', 'user']
        read_only_fields = ['id']


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
            'completed_percentage', 'user', 'resources',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
