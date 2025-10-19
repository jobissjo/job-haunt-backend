from django.db import models
from apis.models.user_management import CustomUser


class LearningManagementStatus(models.Model):
    CATEGORY_CHOICES = [
        ("start", "Start"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]
    name = models.CharField(max_length=20)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    color = models.CharField(max_length=20)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}-{self.category}"


class LearningManagement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    expected_started_date = models.DateField()
    expected_completed_date = models.DateField()
    actual_started_date = models.DateField(null=True, blank=True)
    actual_completed_date = models.DateField(null=True, blank=True)
    status = models.ForeignKey(LearningManagementStatus, on_delete=models.CASCADE, related_name='learning_managements')
    completed_percentage = models.IntegerField(default=0)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}-{self.status.name}"


class LearningResource(models.Model):
    RESOURCE_TYPE_CHOICES = [
        ("video", "Video"),
        ("article", "Article"),
        ("book", "Book"),
        ("course", "Course"),
    ]
    name = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES)
    resource_url = models.URLField()
    learning_management = models.ForeignKey(
        LearningManagement, on_delete=models.CASCADE
    )
    status = models.ForeignKey(LearningManagementStatus, on_delete=models.CASCADE, related_name='learning_resources')
    expected_started_date = models.DateField()
    expected_completed_date = models.DateField()
    actual_started_date = models.DateField(null=True, blank=True)
    actual_completed_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    completed_percentage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
