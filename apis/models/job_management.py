from django.db import models
from .user_management import CustomUser


class JobApplicationStatus(models.Model):
    CATEGORY_CHOICES = [
        ("open", "Open"),
        ("applied", "Applied"),
        ("interview", "Interview"),
        ("offer", "Offer"),
        ("rejected", "Rejected"),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    color = models.CharField(max_length=100)


class JobSkills(models.Model):
    name = models.CharField(max_length=100)


class JobApplication(models.Model):
    APPLICATION_THROUGH_CHOICES = [
        ("email", "Email"),
        ("website", "Website"),
    ]
    position = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    applied_date = models.DateField(null=True, blank=True)
    status = models.ForeignKey(JobApplicationStatus, on_delete=models.CASCADE)
    skills = models.ManyToManyField(JobSkills, related_name="skills")
    preferred_skills = models.ManyToManyField(JobSkills, related_name="preferred_skills")
    description = models.TextField(blank=True, null=True)
    required_experience = models.IntegerField(blank=True, null=True)
    contact_mail = models.EmailField(blank=True, null=True)
    job_posted_date = models.DateField(null=True, blank=True)
    job_closed_date = models.DateField(null=True, blank=True)
    application_through = models.CharField(
        max_length=100, choices=APPLICATION_THROUGH_CHOICES
    )
    application_url = models.URLField(blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.position} - {self.company_name} - {self.location} - {self.applied_date} - {self.status.name}"


class UserSkills(models.Model):
    LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("expert", "Expert"),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    skill = models.ForeignKey(JobSkills, on_delete=models.CASCADE)
    level = models.CharField(max_length=100, choices=LEVEL_CHOICES)
    confidence = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.skill} - {self.level} - {self.confidence}"
