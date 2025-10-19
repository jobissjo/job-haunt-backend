from rest_framework import serializers
from apis import models
from apis.models.user_management import CustomUser, Profile, SocialLink, NotificationPreference, UserEmailSetting
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
    social_links = SocialMediaLinkSerializer(read_only=True)
    
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'phone_number', 'first_name', 
            'last_name', 'role', 'is_active', 'date_joined', 'profile', 'social_links'
        ]
        read_only_fields = ['id', 'date_joined', 'role', ]
    
    
class UserUpdateSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(allow_blank=True, required=False)
    profile_picture = serializers.ImageField(allow_null=True, required=False)
    cover_photo = serializers.ImageField(allow_null=True, required=False)
    linkedin = serializers.URLField(allow_null=True, required=False)
    github = serializers.URLField(allow_null=True, required=False)
    twitter = serializers.URLField(allow_null=True, required=False)
    facebook = serializers.URLField(allow_null=True, required=False)
    instagram = serializers.URLField(allow_null=True, required=False)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'phone_number', 'first_name', 
            'last_name', 'role',  'date_joined', 'bio',  'profile_picture', 'cover_photo', 'linkedin', 'github', 'twitter', 'facebook', 'instagram'
        ]
        read_only_fields = ['id', 'date_joined', 'role', 'email', 'username', 'is_active']

    def update(self, instance, validated_data):
        bio = validated_data.pop('bio')
        profile_picture = validated_data.pop('profile_picture', None)
        cover_photo = validated_data.pop('cover_photo', None)
        linkedin = validated_data.pop('linkedin', None)
        github = validated_data.pop('github', None)
        twitter = validated_data.pop('twitter', None)
        facebook = validated_data.pop('facebook', None)
        instagram = validated_data.pop('instagram', None)

        instance = super().update(instance, validated_data)
        Profile.objects.update_or_create(user=instance, defaults={
            'bio': bio,
            'profile_picture': profile_picture,
            'cover_photo': cover_photo
        })
        SocialLink.objects.update_or_create(user=instance, defaults={
            'linkedin': linkedin,
            'github': github,
            'twitter': twitter,
            'facebook': facebook,
            'instagram': instagram
        })
        return instance

class UpdateUserResumeSerializer(serializers.Serializer):
    resume = serializers.FileField()
    


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


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = ['id', 'user', 'email', 'push', 'in_app', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.push = validated_data.get('push', instance.push)
        instance.in_app = validated_data.get('in_app', instance.in_app)
        instance.save()
        return instance


class UserEmailSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEmailSetting
        fields = ['id', 'user', 'from_email', 'username', 'password', 'use_tls', 'use_ssl', 'host', 'port', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
            is_active = validated_data.get('is_active', False)
            if is_active:
                UserEmailSetting.objects.filter(user=request.user).update(is_active=False)
        else:
            raise serializers.ValidationError("User is not authenticated")
        return super().create(validated_data)
