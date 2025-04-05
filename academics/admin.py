from django.contrib import admin
from django.utils.html import format_html
from .models import (
    AcademicYear, GradeLevel, GradeStream, ClassGroup,
    Department, CourseType, Subject, ClassSubject, 
    TeacherHistory, StudentClassEnrollment, StudentSubjectEnrollment, Promotion
)

# ----- Academic Year ------
@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ("year", "start_date", "end_date")
    search_fields = ("year",)
    ordering = ("year",)

# ----- Grade Level ------
@admin.register(GradeLevel)
class GradeLevelAdmin(admin.ModelAdmin):
    list_display = ("name", "numeric_level")
    search_fields = ("name",)
    ordering = ("numeric_level",)

# ----- Grade Stream ------
@admin.register(GradeStream)
class GradeStreamAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

# ----- Class Group ------
@admin.register(ClassGroup)
class ClassGroupAdmin(admin.ModelAdmin):
    list_display = ("academic_year", "grade", "stream", "homeroom_teacher", "capacity")
    list_filter = ("academic_year", "grade", "stream")
    search_fields = ("academic_year__year", "grade__name", "stream__name", "homeroom_teacher__user__first_name", "homeroom_teacher__user__last_name")
    ordering = ("academic_year", "grade", "stream")

# ----- Department ------
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")

# ----- Course Type ------
@admin.register(CourseType)
class CourseTypeAdmin(admin.ModelAdmin):
    list_display = ("abbreviation", "name", "is_active")
    search_fields = ("name", "abbreviation")
    list_filter = ("is_active",)

# ----- Subject ------
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("course_code", "name", "department", "course_type", "is_active")
    search_fields = ("course_code", "name", "department__name")
    list_filter = ("department", "course_type", "is_active")

# ----- Class Subject ------
class TeacherHistoryInline(admin.TabularInline):
    model = TeacherHistory
    extra = 0
    readonly_fields = ("teacher", "start_date", "end_date", "reason")

@admin.register(ClassSubject)
class ClassSubjectAdmin(admin.ModelAdmin):
    list_display = ("class_group", "subject", "teacher", "start_date", "end_date")
    search_fields = ("class_group__grade__name", "class_group__stream__name", "subject__name", "teacher__user__first_name", "teacher__user__last_name")
    list_filter = ("class_group__academic_year", "subject")
    inlines = [TeacherHistoryInline]

# ----- Student Class Enrollment ------
class StudentSubjectEnrollmentInline(admin.TabularInline):
    model = StudentSubjectEnrollment
    extra = 0
    readonly_fields = ("student", "class_subject")

@admin.register(StudentClassEnrollment)
class StudentClassEnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "class_group", "date_enrolled", "enrolled_subjects")
    list_filter = ("class_group", "date_enrolled")
    search_fields = ("student__user__first_name", "student__user__last_name", "class_group__grade__name")

    def enrolled_subjects(self, obj):
        subjects = obj.student.studentsubjectenrollment_set.all()
        return format_html("<br>".join([s.class_subject.subject.name for s in subjects]))
    
    enrolled_subjects.short_description = "Enrolled Subjects"


# ----- Student Subject Enrollment ------
@admin.register(StudentSubjectEnrollment)
class StudentSubjectEnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "class_subject")
    search_fields = ("student__user__first_name", "student__user__last_name", "class_subject__subject__name")
    list_filter = ("class_subject__class_group__academic_year", "class_subject__subject")

# ----- Promotion ------
@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ("student", "from_class", "to_class", "promoted_on")
    search_fields = ("student__user__first_name", "student__user__last_name", "from_class__grade__name", "to_class__grade__name")
    list_filter = ("from_class__academic_year",)

