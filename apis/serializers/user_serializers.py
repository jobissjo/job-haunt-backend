from rest_framework import serializers
from apis import models
from apis.models.user_management import CustomUser, Profile, SocialLink
from apis.models.job_management import UserSkills, JobSkills


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'bio', 'profile_picture', 'cover_photo']


class SocialMediaLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = '__all__'
        read_only_fields = ['id', 'user']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    social_links = SocialMediaLinkSerializer(allow_null=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'phone_number', 'first_name', 
            'last_name', 'role', 'is_active', 'date_joined', 'profile', 'social_links'
        ]
        read_only_fields = ['id', 'date_joined', 'role', ]
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        social_links_data = validated_data.pop('social_links')
        user = CustomUser.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        SocialLink.objects.create(user=user, **social_links_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        social_links_data = validated_data.pop('social_links')
        instance = super().update(instance, validated_data)
        Profile.objects.update_or_create(user=instance, defaults=profile_data)
        SocialLink.objects.update_or_create(user=instance, defaults=social_links_data)
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'phone_number', 'first_name', 
            'last_name', 'password', 'password_confirm'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(password=password, **validated_data)
        # Create profile automatically
        Profile.objects.create(user=user)
        return user


class JobSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSkills
        fields = ['id', 'name']


class UserSkillsSerializer(serializers.ModelSerializer):
    skill_detail = JobSkillsSerializer(source='skill', read_only=True)
    skill = serializers.PrimaryKeyRelatedField(queryset=JobSkills.objects.all())
    
    class Meta:
        model = UserSkills
        fields = ['id', 'user', 'skill', 'skill_detail', 'level', 'confidence', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user', 'skill']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        else:
            raise serializers.ValidationError("User is not authenticated")
        return super().create(validated_data)