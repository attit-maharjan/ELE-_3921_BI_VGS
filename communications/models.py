from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from users.models import User  # Import directly

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    


User = get_user_model()

class AnnouncementCategory(models.Model):
    """Categories for announcements, customizable per school."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Announcement(models.Model):
    """Public announcements posted by teachers, staff, or stakeholders."""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('draft', 'Draft'),
    ]

    title = models.CharField(max_length=255)
    message = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="announcements")
    category = models.ForeignKey(AnnouncementCategory, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=now)
    deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def is_expired(self):
        """Check if the announcement has expired based on deadline."""
        return self.deadline and self.deadline < now()
