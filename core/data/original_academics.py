# BIVGS>academics>models.py


from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils import timezone

# ----- AcademicYear Class ------
class AcademicYear(models.Model):
    year = models.IntegerField(unique=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Academic Year {self.year}"

# ----- Classroom Class ------
class Classroom(models.Model):
    grade = models.IntegerField()
    section = models.CharField(max_length=10)
    capacity = models.IntegerField()

    def __str__(self):
        return f"Grade {self.grade} - {self.section}"
    
class CourseType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=10, unique=True)  # New field for short codes
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)  # Whether the variant is active or not

    def __str__(self):
        return f"{self.abbreviation} - {self.name}"

    class Meta:
        verbose_name = "Course Type"
        verbose_name_plural = "Course Types"


# ----- Department Class ------
class Department(models.Model):
    code = models.CharField(max_length=10, unique=True)  # Example: 'MTH', 'SCI', 'ENG'
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)  

    def __str__(self):
        return f"{self.code} - {self.name}"


    def __str__(self):
        return f"{self.code} - {self.name}"


# ----- Subject Class ------

class Subject(models.Model):
    course_code_validator = RegexValidator(
        regex=r'^[A-Za-z]{3}-\d{3}$',  # 3 letters, dash, 3 numbers
        message="Course code must be in the format 'AAA-111'."
    )

    name = models.CharField(max_length=100)
    course_code = models.CharField(
        max_length=10,
        unique=True,
        default="AAA-111",
        validators=[course_code_validator]
    )
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)  # ForeignKey to Department
    grade_level = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True)
    course_type = models.ForeignKey(CourseType, on_delete=models.SET_NULL, null=True, blank=True)
    date_registered = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        grade_level_str = f"Grade {self.grade_level.grade} {self.grade_level.section}" if self.grade_level else "No Grade Level"
        course_type_str = f"[{self.course_type}]" if self.course_type else "No Course Type"
        # Check if department exists, if not, set it to 'No Department'
        department_str = self.department.name if self.department else "No Department"
        return f"{self.course_code} ({department_str}) - {self.name} ({grade_level_str}) {course_type_str}"

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"




# ----- ClassSubject Class ------
class ClassSubject(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey('users.Teacher', on_delete=models.CASCADE, limit_choices_to={'user__role': 'teacher'})
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['academic_year', 'classroom', 'subject'], name='unique_class_subject')
        ]

    def __str__(self):
        return f"{self.subject.name} - {self.teacher.user.first_name} {self.teacher.user.last_name} ({self.academic_year.year})"

# ----- StudentEnrollment Class ------
class StudentEnrollment(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    date_enrolled = models.DateField()

    def __str__(self):
        return f"{self.student.user.first_name} {self.student.user.last_name} - {self.academic_year.year}"

# ----- StudentSubjectEnrollment Class ------
class StudentSubjectEnrollment(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    grade = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.first_name} {self.student.user.last_name} - {self.subject.name} ({self.academic_year.year})"

# ----- StudentProgression Class ------
class StudentProgression(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    from_year = models.ForeignKey(AcademicYear, related_name="from_year", on_delete=models.CASCADE)
    to_year = models.ForeignKey(AcademicYear, related_name="to_year", on_delete=models.CASCADE)
    progression_date = models.DateField()

    def __str__(self):
        return f"{self.student.user.first_name} {self.student.user.last_name} - {self.from_year.year} to {self.to_year.year}"
