from rest_framework import serializers
from apis.models.job_management import JobApplicationStatus, JobSkills, JobApplication


class JobApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplicationStatus
        fields = ['id', 'name', 'category', 'color']


class JobSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSkills
        fields = ['id', 'name']


class JobApplicationSerializer(serializers.ModelSerializer):
    status_detail = JobApplicationStatusSerializer(source='status', read_only=True)
    skills_detail = JobSkillsSerializer(source='skills', many=True, read_only=True)
    preferred_skills_detail = JobSkillsSerializer(source='preferred_skills', many=True, read_only=True)
    preferred_skills = serializers.PrimaryKeyRelatedField(queryset=JobSkills.objects.all(), many=True, required=False, allow_null=True)
    skills = serializers.PrimaryKeyRelatedField(queryset=JobSkills.objects.all(), many=True, required=False, allow_null=True)
    
    class Meta:
        model = JobApplication
        fields = [
            'id', 'position', 'company_name', 'location', 'applied_date',
            'status', 'status_detail', 'skills', 'skills_detail',
            'preferred_skills', 'preferred_skills_detail', 'description',
            'required_experience', 'contact_mail', 'job_posted_date',
            'job_closed_date', 'application_through', 'application_url',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']


class JobApplicationCreateSerializer(serializers.ModelSerializer):
    preferred_skills = serializers.PrimaryKeyRelatedField(queryset=JobSkills.objects.all(), many=True, required=False, allow_null=True)
    skills = serializers.PrimaryKeyRelatedField(queryset=JobSkills.objects.all(), many=True, required=False, allow_null=True)
    class Meta:
        model = JobApplication
        fields = [
            'position', 'company_name', 'location', 'applied_date',
            'status', 'skills', 'preferred_skills', 'description',
            'required_experience', 'contact_mail', 'job_posted_date',
            'job_closed_date', 'application_through', 'application_url',
        ]
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)
