# ########## users > models.py
# users app > models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import date, timedelta
import uuid

from core.models import SchoolSettings
from academics.models import Subject, Department


# Phone number validator (supports international format)
phone_validator = RegexValidator(
    regex=r'^\+?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)


class CustomUserManager(BaseUserManager):
    """Manager for Custom User Model"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class Address(models.Model):
    """Allow multiple users to share an address"""
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state_province}, {self.country}"


class User(AbstractUser):
    """Custom User Model"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
        ('staff', 'Staff'),
        ('stakeholder', 'Stakeholder'),
    ]

    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    initials = models.CharField(max_length=10, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    dob = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, validators=[phone_validator])
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=False, default='student')
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    groups = models.ManyToManyField(Group, related_name="custom_user_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions_set", blank=True)

    def clean(self):
        """Validate age restrictions for students and ensure DOB is not in the future for all users"""
        if self.dob:
            if self.dob > date.today():
                raise ValidationError("Date of birth cannot be in the future.")

            if self.role == "student":
                school_settings = SchoolSettings.objects.first()
                if school_settings:
                    age = (date.today() - self.dob).days // 365
                    if age < school_settings.min_age or age > school_settings.max_age:
                        raise ValidationError(
                            f"Student age must be between {school_settings.min_age} and {school_settings.max_age} years."
                        )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"


class Student(models.Model):
    """Student Model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    student_id = models.CharField(max_length=20, unique=True, blank=True, editable=False)
    parents = models.ManyToManyField('Parent', related_name='students', blank=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            self.user.role = "student"
            self.user.save(update_fields=['role'])

        if not self.student_id:
            self.student_id = f"S{date.today().year}{uuid.uuid4().hex[:8].upper()}"


        super().save(*args, **kwargs)


    def __str__(self):
        return f"Student: {self.user.first_name} {self.user.last_name}"


class Parent(models.Model):
    """Parent Model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alternative_phone_number = models.CharField(max_length=15, blank=True, null=True, validators=[phone_validator])

    def __str__(self):
        return f"Parent: {self.user.first_name} {self.user.last_name}"


class Teacher(models.Model):
    """Teacher Model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    departments = models.ManyToManyField(Department, related_name="teachers")
    subject_specialization = models.ManyToManyField(Subject, related_name="specialist_teachers")
    hire_date = models.DateField(auto_now_add=True)
    employee_id = models.CharField(max_length=20, unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        self.user.role = "teacher"
        self.user.save(update_fields=['role'])

        if not self.employee_id:
            self.employee_id = f"T{date.today().year}{uuid.uuid4().hex[:8].upper()}"

        super().save(*args, **kwargs)

        if is_new:
            TeacherEmploymentHistory.objects.create(teacher=self, start_date=self.hire_date)

    def __str__(self):
        return f"Teacher: {self.user.first_name} {self.user.last_name}"


class TeacherEmploymentHistory(models.Model):
    """Track the employment history of teachers"""
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="employment_history")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    reason_for_leaving = models.TextField(blank=True, null=True)

    def clean(self):
        if self.end_date and (self.end_date < self.start_date or self.end_date > date.today()):
            raise ValidationError("Invalid end date.")

        if TeacherEmploymentHistory.objects.filter(
            teacher=self.teacher,
            start_date__lte=self.end_date or date.today(),
            end_date__gte=self.start_date,
        ).exclude(pk=self.pk).exists():
            raise ValidationError("Teacher already has an overlapping employment record.")

    def __str__(self):
        return f"{self.teacher.user.first_name} {self.teacher.user.last_name} ({self.start_date} - {self.end_date or 'Present'})"


class Staff(models.Model):
    """Staff Model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_role = models.CharField(max_length=100)
    hire_date = models.DateField(auto_now_add=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Staff: {self.user.first_name} {self.user.last_name}"



class StakeholderType(models.Model):
    """Stakeholder Type Model"""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Stakeholder(models.Model):
    """Stakeholder Model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stakeholder_types = models.ManyToManyField(StakeholderType, related_name="stakeholders")
    relationship_to_school = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Stakeholder: {self.user.first_name} {self.user.last_name}"








