from django.contrib import admin
from .models import Exam, ExamResult, GradeDistribution

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('subject', 'academic_year', 'exam_type', 'exam_date')

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'score', 'grade')

@admin.register(GradeDistribution)
class GradeDistributionAdmin(admin.ModelAdmin):
    list_display = ('exam', 'average_score', 'highest_score', 'lowest_score')