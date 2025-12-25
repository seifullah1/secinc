from django.conf import settings
from django.db import models
from django.utils import timezone

class Incident(models.Model):
    class Category(models.TextChoices):
        PHISHING = "phishing", "Phishing"
        MALWARE = "malware", "Malware"
        UNAUTHORIZED = "unauthorized", "Unauthorized access"
        DATA_LEAK = "data_leak", "Data leak"
        DDOS = "ddos", "DDoS"
        OTHER = "other", "Other"

    class Severity(models.IntegerChoices):
        LOW = 1, "Low"
        MEDIUM = 2, "Medium"
        HIGH = 3, "High"
        CRITICAL = 4, "Critical"

    class Status(models.TextChoices):
        NEW = "new", "New"
        IN_PROGRESS = "in_progress", "In progress"
        RESOLVED = "resolved", "Resolved"
        CLOSED = "closed", "Closed"

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    category = models.CharField(max_length=30, choices=Category.choices, default=Category.OTHER)
    severity = models.IntegerField(choices=Severity.choices, default=Severity.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)

    asset = models.CharField(max_length=120, blank=True)
    detected_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="reported_incidents"
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True, related_name="assigned_incidents"
    )

    def close(self):
        self.status = self.Status.CLOSED
        self.closed_at = timezone.now()

    def __str__(self):
        return f"#{self.id} {self.title}"
    
class SecurityEvent(models.Model):
    class EventType(models.TextChoices):
        LOGIN_SUCCESS = "login_success", "Login success"
        LOGIN_FAILED = "login_failed", "Login failed"

    event_type = models.CharField(max_length=40, choices=EventType.choices)
    username = models.CharField(max_length=150, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )

    ip_address = models.CharField(max_length=64, blank=True)
    user_agent = models.TextField(blank=True)
    path = models.CharField(max_length=255, blank=True)
    is_admin_panel = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at} {self.event_type} {self.username} {self.ip_address}"
class LoginLock(models.Model):
    username = models.CharField(max_length=150, blank=True)
    ip_address = models.CharField(max_length=64, blank=True)

    failed_count = models.PositiveIntegerField(default=0)
    window_started_at = models.DateTimeField(default=timezone.now)
    locked_until = models.DateTimeField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["username", "ip_address"]),
            models.Index(fields=["locked_until"]),
        ]

    def is_locked(self):
        return self.locked_until is not None and self.locked_until > timezone.now()

    def __str__(self):
        return f"Lock(username={self.username}, ip={self.ip_address}, locked_until={self.locked_until})"
