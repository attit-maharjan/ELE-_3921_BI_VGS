# BIVGS>academics>models.py
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator


# ----- Academic Year ------
class AcademicYear(models.Model):
    year = models.IntegerField(unique=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Academic Year {self.year}"


# ----- Grade Level ------
class GradeLevel(models.Model):
    name = models.CharField(max_length=20, unique=True)
    numeric_level = models.IntegerField(unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["numeric_level"]

    def __str__(self):
        return self.name


# ----- Grade Stream ------
class GradeStream(models.Model):
    name = models.CharField(max_length=10, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ----- Class Group ------
class ClassGroup(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    grade = models.ForeignKey(GradeLevel, on_delete=models.PROTECT)
    stream = models.ForeignKey(GradeStream, on_delete=models.PROTECT)
    capacity = models.IntegerField()

    homeroom_teacher = models.ForeignKey(
        "users.Teacher",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="homeroom_classes",
    )

    student_representative = models.ForeignKey(
        "users.Student",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="representative_class",
    )

    class Meta:
        unique_together = ("academic_year", "grade", "stream")

    def __str__(self):
        return f"{self.grade.name} {self.stream.name} of {self.academic_year.year}"


# ----- Department ------
class Department(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


# ----- Course Type ------
class CourseType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=10, unique=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.abbreviation} - {self.name}"

    class Meta:
        verbose_name = "Course Type"
        verbose_name_plural = "Course Types"


# ----- Subject ------
class Subject(models.Model):
    course_code_validator = RegexValidator(
        regex=r'^[A-Z]{2,5}-\d{2,5}$',
        message="Course code must be in the format 'XX-111' or 'XXXXX-11111'."
    )

    name = models.CharField(max_length=100)
    course_code = models.CharField(
        max_length=10,
        unique=True,
        validators=[course_code_validator]
    )
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    course_type = models.ForeignKey(CourseType, on_delete=models.SET_NULL, null=True, blank=True)
    date_registered = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.course_code} ({self.department.name if self.department else 'No Department'}) - {self.name}"


# ----- Class Subject (Current Teacher) ------
class ClassSubject(models.Model):
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE, related_name="subjects")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        "users.Teacher",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="current_teaching_classes"
    )
    start_date = models.DateField(default=timezone.now)  # Track when a teacher starts
    end_date = models.DateField(null=True, blank=True)  # Optional: Used when a subject is discontinued

    class Meta:
        unique_together = ("class_group", "subject")

    def __str__(self):
        teacher_name = f"{self.teacher.user.first_name} {self.teacher.user.last_name}" if self.teacher else "No Teacher"
        return f"{self.subject.name} - {teacher_name} ({self.class_group})"

    def save(self, *args, **kwargs):
        if self.pk:  # If updating an existing record
            old_instance = ClassSubject.objects.get(pk=self.pk)
            if old_instance.teacher != self.teacher:
                # Log the history before updating
                TeacherHistory.objects.create(
                    class_subject=old_instance,
                    teacher=old_instance.teacher,
                    start_date=old_instance.start_date,
                    end_date=timezone.now(),
                    reason="Teacher changed"
                )
                # Reset start date for the new teacher
                self.start_date = timezone.now()
        
        super().save(*args, **kwargs)



# ----- Teacher History ------
class TeacherHistory(models.Model):
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE, related_name="teacher_history")
    teacher = models.ForeignKey("users.Teacher", on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    reason = models.CharField(max_length=255, choices=[
        ("left_temporarily", "Left Temporarily"),
        ("left_permanently", "Left Permanently"),
        ("deceased", "Deceased"),
        ("teacher_changed", "Teacher Changed")
    ])

    def __str__(self):
        return f"{self.teacher} ({self.reason}) from {self.start_date} to {self.end_date or 'Present'}"


# ----- Student Class Enrollment ------
class StudentClassEnrollment(models.Model):
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE, related_name="enrollments")
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ("student", "class_group")

    def __str__(self):
        return f"{self.student} - {self.class_group}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for class_subject in self.class_group.subjects.all():
            StudentSubjectEnrollment.objects.get_or_create(
                student=self.student,
                class_subject=class_subject
            )


# ----- Student Subject Enrollment ------
class StudentSubjectEnrollment(models.Model):
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE)   

    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE, default=1)  # temporary default. default=1, remove after successful migrations

    def __str__(self):
        return f"{self.student} - {self.class_subject.subject}"


# ----- Promotion ------
class Promotion(models.Model):
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE, related_name="promotions")
    from_class = models.ForeignKey(ClassGroup, on_delete=models.CASCADE, related_name="promotions_from")
    to_class = models.ForeignKey(ClassGroup, on_delete=models.CASCADE, related_name="promotions_to", null=True, blank=True)
    promoted_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} promoted from {self.from_class} to {self.to_class if self.to_class else 'Graduated'}"




###############################

# from django.db import models
# from django.conf import settings
# from django.core.validators import RegexValidator
# from django.utils import timezone

# # ----- AcademicYear Class ------
# class AcademicYear(models.Model):
#     year = models.IntegerField(unique=True)
#     start_date = models.DateField()
#     end_date = models.DateField()

#     def __str__(self):
#         return f"Academic Year {self.year}"
    
    
# # ----- GradeLevel Class ------
# class GradeLevel(models.Model):
#     name = models.CharField(max_length=20, unique=True)  # Example: 'Grade 9', 'Year 1', 'Form 3'
#     numeric_level = models.IntegerField(unique=True)  # Example: 9, 10, 11
#     description = models.TextField(null=True, blank=True)

#     class Meta:
#         ordering = ['numeric_level']  # Ensures grades are ordered properly

#     def __str__(self):
#         return self.name
    



# # ----- GradeStream Class ------
# class GradeStream(models.Model):
#     name = models.CharField(max_length=10, unique=True)  # Example: 'A', 'B', 'C', 'Red', 'Blue'
#     description = models.TextField(null=True, blank=True)

#     class Meta:
#         ordering = ['name']  # Ensures alphabetical order

#     def __str__(self):
#         return self.name


# # ----- ClassGroup Class ------
# class ClassGroup(models.Model):
#     academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
#     grade = models.ForeignKey(GradeLevel, on_delete=models.PROTECT)  # Prevent deletion if in use
#     stream = models.ForeignKey(GradeStream, on_delete=models.PROTECT)  # Link to predefined streams
#     capacity = models.IntegerField()

#     class Meta:
#         unique_together = ('academic_year', 'grade', 'stream')

#     def __str__(self):
#         return f"{self.academic_year.year} - {self.grade.name} {self.stream.name}"

# # ----- CourseType Class ------  
# class CourseType(models.Model):
#     name = models.CharField(max_length=50, unique=True)
#     abbreviation = models.CharField(max_length=10, unique=True)  # New field for short codes
#     description = models.TextField(null=True, blank=True)
#     is_active = models.BooleanField(default=True)  # Whether the variant is active or not

#     def __str__(self):
#         return f"{self.abbreviation} - {self.name}"

#     class Meta:
#         verbose_name = "Course Type"
#         verbose_name_plural = "Course Types"


# # ----- Department Class ------
# class Department(models.Model):
#     code = models.CharField(max_length=10, unique=True)  # Example: 'MTH', 'SCI', 'ENG'
#     name = models.CharField(max_length=100, unique=True)
#     description = models.TextField(null=True, blank=True)  

#     def __str__(self):
#         return f"{self.code} - {self.name}"


#     def __str__(self):
#         return f"{self.code} - {self.name}"


# # ----- Subject Class ------
# class Subject(models.Model):
#     course_code_validator = RegexValidator(
#         regex=r'^[A-Za-z]{3}-\d{3}$',  
#         message="Course code must be in the format 'AAA-111'."
#     )

#     name = models.CharField(max_length=100)
#     course_code = models.CharField(
#         max_length=10,
#         unique=True,
#         validators=[course_code_validator]
#     )
#     department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
#     course_type = models.ForeignKey(CourseType, on_delete=models.SET_NULL, null=True, blank=True)
#     date_registered = models.DateField(default=timezone.now)
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return f"{self.course_code} ({self.department.name if self.department else 'No Department'}) - {self.name}"

# # ----- SubjectAssignment Class ------
# class SubjectAssignment(models.Model):
#     class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE, related_name="subjects", null=True, blank=True)
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('class_group', 'subject')

#     def __str__(self):
#         return f"{self.class_group} - {self.subject}"





# # ----- ClassSubject Class ------
# class ClassSubject(models.Model):
#     class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE, null=True, blank=True)
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     teacher = models.ForeignKey('users.Teacher', on_delete=models.CASCADE, limit_choices_to={'user__role': 'teacher'})

#     class Meta:
#         unique_together = ('class_group', 'subject')

#     def __str__(self):
#         return f"{self.subject.name} - {self.teacher.user.first_name} {self.teacher.user.last_name} ({self.class_group})"


# # ----- StudentClassEnrollment Class ------
# class StudentClassEnrollment(models.Model):
#     student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name="enrollments")
#     class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE)
#     date_enrolled = models.DateField(default=timezone.now)

#     class Meta:
#         unique_together = ('student', 'class_group')

#     def __str__(self):
#         return f"{self.student} - {self.class_group}"


# # ----- StudentSubjectEnrollment Class ------
# class StudentSubjectEnrollment(models.Model):
#     student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
#     subject_assignment = models.ForeignKey(SubjectAssignment, on_delete=models.CASCADE, null=True, blank=True)
#     grade = models.CharField(max_length=10, null=True, blank=True)

#     def __str__(self):
#         return f"{self.student} - {self.subject_assignment}"


# # ----- Student Progression ------
# # ----- Promotion Class ------
# class Promotion(models.Model):
#     student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name="promotions")
#     from_class = models.ForeignKey(ClassGroup, on_delete=models.CASCADE, related_name="promotions_from")
#     to_class = models.ForeignKey(ClassGroup, on_delete=models.CASCADE, related_name="promotions_to", null=True, blank=True)
#     promoted_on = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.student} promoted from {self.from_class.grade.name} to {self.to_class.grade.name if self.to_class else 'Graduated'}"
