from django.db import models
from users.models import Student, Teacher  # Import directly
from academics.models import AcademicYear  # Import directly

class ReportCard(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    subject_results = models.JSONField()  # Store results per subject
    overall_grade = models.CharField(max_length=10)
    report_generated_date = models.DateField()

class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    feedback_date = models.DateField()
    feedback_text = models.TextField()