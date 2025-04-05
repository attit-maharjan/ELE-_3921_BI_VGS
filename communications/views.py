from django.shortcuts import render, get_object_or_404
from .models import Announcement

def announcements_list(request):
    """Fetch only active announcements."""
    announcements = Announcement.objects.filter(status='active').order_by('-created_at')
    return render(request, 'communications/announcements_list.html', {'active_announcements': announcements})

def announcement_detail(request, pk):
    """Fetch a single announcement by ID."""
    announcement = get_object_or_404(Announcement, pk=pk)
    return render(request, 'communications/announcement_detail.html', {'announcement': announcement})

def post_event(request):
    return render()