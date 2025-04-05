from django.db import models
from academics.models import Subject, AcademicYear  # Directly importing models

class Exam(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=50)
    exam_date = models.DateField()

class ExamResult(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=10)

class GradeDistribution(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    average_score = models.DecimalField(max_digits=5, decimal_places=2)
    highest_score = models.DecimalField(max_digits=5, decimal_places=2)
    lowest_score = models.DecimalField(max_digits=5, decimal_places=2)
    percentiles = models.JSONField()  # Stores percentiles for analysis