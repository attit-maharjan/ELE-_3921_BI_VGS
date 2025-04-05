from django.contrib import admin
from .models import ReportCard, Feedback

@admin.register(ReportCard)
class ReportCardAdmin(admin.ModelAdmin):
    list_display = ('student', 'academic_year', 'overall_grade', 'report_generated_date')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('student', 'teacher', 'feedback_date', 'feedback_text')