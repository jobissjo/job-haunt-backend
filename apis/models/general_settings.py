from django.db import models
from django.utils import timezone

class EmailProviderSetting(models.Model):
    PROVIDER_TYPES = [
        ("smtp", "SMTP"),
        ("sendgrid", "SendGrid"),
        ("mailgun", "Mailgun"),
        ("ses", "Amazon SES"),
    ]

    name = models.CharField(max_length=50, unique=True)
    provider_type = models.CharField(max_length=20, choices=PROVIDER_TYPES)
    host = models.CharField(max_length=255, blank=True, null=True)
    port = models.PositiveIntegerField(blank=True, null=True)
    from_email = models.EmailField()
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    use_tls = models.BooleanField(default=True)
    use_ssl = models.BooleanField(default=False)
    api_key = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Ensure only one active provider at a time
        if self.is_active:
            EmailProviderSetting.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.name} ({self.provider_type})"


class EmailLog(models.Model):
    subject = models.CharField(max_length=255)
    body = models.JSONField()
    to = models.CharField(max_length=255)
    email_provider = models.ForeignKey(EmailProviderSetting, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.subject} - {self.status}"
