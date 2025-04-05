from django.urls import path
from . import views


app_name = 'communications'

urlpatterns = [
    path('', views.announcements_list, name='announcements_list'),
    path('announcement/<int:pk>/', views.announcement_detail, name='announcement_detail'),
    path('post_event/', views.post_event, name='post_event')
]
