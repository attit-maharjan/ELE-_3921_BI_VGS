from django.contrib import admin
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from .models import SchoolSettings, Accreditor
from django.utils.translation import gettext_lazy as _

# Customizing the display of Accreditor model in admin
class AccreditorAdmin(admin.ModelAdmin):
    list_display = ('name', 'registration_number', 'status', 'accreditation_date', 'website')
    search_fields = ('name', 'registration_number')
    list_filter = ('status',)
    ordering = ('name',)

    # Add fieldsets to group fields logically in the admin form
    fieldsets = (
        (None, {
            'fields': ('name', 'registration_number', 'status')
        }),
        (_('Accreditation Details'), {
            'fields': ('accreditation_date', 'website')
        }),
    )

# Customizing the display of SchoolSettings model in admin
class SchoolSettingsAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'school_motto', 'established_year', 'contact_number', 'principal_name', 'min_age', 'max_age')
    search_fields = ('school_name', 'principal_name')
    list_filter = ('established_year',)
    ordering = ('school_name',)

    # Add fieldsets to group fields logically in the admin form
    fieldsets = (
        (None, {
            'fields': ('school_name', 'school_logo', 'school_motto', 'established_year')
        }),
        (_('Contact Details'), {
            'fields': ('address', 'contact_number', 'email_address', 'website_url')
        }),
        (_('Principal and Accreditation'), {
            'fields': ('principal_name', 'accreditation_details')
        }),
        (_('Social Media and Age Settings'), {
            'fields': ('social_media_links', 'min_age', 'max_age')
        }),
    )

    # Ensure only one entry of SchoolSettings exists
    def save_model(self, request, obj, form, change):
        # Enforce single entry rule
        if not change and SchoolSettings.objects.exists():
            raise ValidationError("Only one SchoolSettings entry is allowed.")
        super().save_model(request, obj, form, change)

    # Display the uploaded logo in the admin interface
    def display_logo(self, obj):
        """Display the uploaded school logo in the Django Admin panel while maintaining aspect ratio."""
        if obj.school_logo:
            return format_html('<img src="{}" width="100" height="auto" style="border-radius:10px;" />', obj.school_logo.url)
        return "No Logo Uploaded"
    
    display_logo.short_description = "School Logo"
    
# Register models with their custom admin classes
admin.site.register(Accreditor, AccreditorAdmin)
admin.site.register(SchoolSettings, SchoolSettingsAdmin)
