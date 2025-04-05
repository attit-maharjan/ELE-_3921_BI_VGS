from django.db import models
from django.core.exceptions import ValidationError

def school_logo_upload_path(instance, filename):
    """Ensure the school logo is stored in the media directory with a proper filename."""
    return f"school_logos/{instance.school_name.replace(' ', '_').lower()}_{filename}"

class Accreditor(models.Model):
    """Stores details of organizations accrediting schools."""
    name = models.CharField(max_length=255, unique=True)
    registration_number = models.CharField(max_length=100, unique=True, help_text="Accreditor's unique ID")
    website = models.URLField(blank=True, null=True)
    accreditation_date = models.DateField()
    
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Expired", "Expired"),
        ("Pending", "Pending")
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Active")

    def __str__(self):
        return f"{self.name} ({self.status})"

class SchoolSettings(models.Model):
    """Stores school-specific settings (ensuring only one entry exists)."""
    school_name = models.CharField(max_length=255, unique=True)
    school_logo = models.ImageField(upload_to=school_logo_upload_path, blank=True, null=True)
    school_motto = models.CharField(max_length=255, blank=True, null=True)
    established_year = models.PositiveIntegerField(blank=True, null=True)
    address = models.TextField()
    contact_number = models.CharField(max_length=20)
    email_address = models.EmailField()
    website_url = models.URLField(blank=True, null=True)
    principal_name = models.CharField(max_length=255)
    accreditation_details = models.ManyToManyField(Accreditor, blank=True, related_name="schools")
    social_media_links = models.JSONField(blank=True, null=True, help_text="Store links as JSON")
    
    min_age = models.PositiveIntegerField(default=6, help_text="Minimum age for learners")
    max_age = models.PositiveIntegerField(default=18, help_text="Maximum age for learners")


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """Ensure only one SchoolSettings entry exists."""
        if SchoolSettings.objects.exists() and not self.pk:
            raise ValidationError("Only one School Settings entry is allowed.")

    def __str__(self):
        return self.school_name

