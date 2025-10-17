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
    
    class Meta:
        model = JobApplication
        fields = [
            'id', 'position', 'company_name', 'location', 'applied_date',
            'status', 'status_detail', 'skills', 'skills_detail',
            'preferred_skills', 'preferred_skills_detail', 'description',
            'required_experience', 'contact_mail', 'job_posted_date',
            'job_closed_date', 'application_through', 'application_url',
            'user', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class JobApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = [
            'position', 'company_name', 'location', 'applied_date',
            'status', 'skills', 'preferred_skills', 'description',
            'required_experience', 'contact_mail', 'job_posted_date',
            'job_closed_date', 'application_through', 'application_url', 'user'
        ]
    
    def validate(self, attrs):
        # Ensure user can only create applications for themselves
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            if attrs.get('user') != request.user and not request.user.is_staff:
                raise serializers.ValidationError({"user": "You can only create applications for yourself"})
        return attrs
