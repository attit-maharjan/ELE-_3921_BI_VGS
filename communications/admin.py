from django.contrib import admin
from .models import Announcement, AnnouncementCategory, Message, Notification

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'sent_at', 'message_body')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'sent_at', 'is_read')
    


@admin.register(AnnouncementCategory)
class AnnouncementCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'deadline', 'status')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'message')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        """Limit announcement creation to staff, teachers, and stakeholders"""
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.role in ['teacher', 'staff', 'stakeholder']:
            return qs
        return qs.none()
