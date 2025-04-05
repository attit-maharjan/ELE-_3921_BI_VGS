from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    User, Student, Teacher, Parent, Staff, Stakeholder, StakeholderType,
    Address, TeacherEmploymentHistory
)

### Custom User Admin ###
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('date_joined',)
    readonly_fields = ('date_joined', 'role')  # Role should not be manually edited

    fieldsets = (
        (_("Personal Info"), {"fields": ("email", "first_name", "last_name", "dob", "phone_number", "address")}),
        (_("Roles & Permissions"), {"fields": ("role", "is_active", "groups", "user_permissions")}),
        (_("Security"), {"fields": ("password",)}),
    )
    
    add_fieldsets = (
        (_("Create New User"), {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "role", "password1", "password2"),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        """Make role read-only only when editing an existing user, except for superusers"""
        if obj and not request.user.is_superuser:  # Only non-superusers have role as read-only
            return ('role', 'date_joined')
        return ('date_joined',)  # If creating a new user


### Student Admin ###
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'user', 'enrollment_date', 'list_parents')
    list_filter = ('enrollment_date',)
    search_fields = ('student_id', 'user__first_name', 'user__last_name', 'user__email')
    ordering = ('enrollment_date',)
    readonly_fields = ('student_id', 'enrollment_date')

    filter_horizontal = ('parents',)  # Allow easy selection of multiple parents

    def list_parents(self, obj):
        return ", ".join([parent.user.get_full_name() for parent in obj.parents.all()])
    list_parents.short_description = "Parents"


### Parent Admin ###
class ParentAdmin(admin.ModelAdmin):
    list_display = ('user', 'alternative_phone_number')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'alternative_phone_number')


### TeacherEmploymentHistory Inline Admin ###
class TeacherEmploymentHistoryInline(admin.TabularInline):
    model = TeacherEmploymentHistory
    extra = 1  # Allows adding history inline
    readonly_fields = ('start_date',)  # Start date should not be modified after creation


### Teacher Admin ###
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'user', 'hire_date', 'list_departments', 'list_subjects')
    list_filter = ('hire_date', 'departments')
    search_fields = ('employee_id', 'user__first_name', 'user__last_name', 'user__email')
    readonly_fields = ('employee_id', 'hire_date')

    inlines = [TeacherEmploymentHistoryInline]  # Show employment history inline

    def list_departments(self, obj):
        return ", ".join([dept.name for dept in obj.departments.all()])
    list_departments.short_description = "Departments"

    def list_subjects(self, obj):
        return ", ".join([subject.name for subject in obj.subject_specialization.all()])
    list_subjects.short_description = "Subjects"


### TeacherEmploymentHistory Admin ###
class TeacherEmploymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'start_date', 'end_date', 'reason_for_leaving')
    list_filter = ('start_date', 'end_date')
    search_fields = ('teacher__user__first_name', 'teacher__user__last_name', 'teacher__employee_id')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = Teacher.objects.select_related("user").all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


### Staff Admin ###
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'staff_role', 'hire_date')
    list_filter = ('hire_date', 'staff_role')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')


### Stakeholder Admin ###
class StakeholderAdmin(admin.ModelAdmin):
    list_display = ('user', 'list_stakeholder_types', 'relationship_to_school')
    list_filter = ('stakeholder_types',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email')

    def list_stakeholder_types(self, obj):
        return ", ".join([s.name for s in obj.stakeholder_types.all()])
    list_stakeholder_types.short_description = "Stakeholder Types"


### Stakeholder Type Admin ###
class StakeholderTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


### Address Admin ###
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street_address', 'city', 'state_province', 'country')
    search_fields = ('street_address', 'city', 'state_province', 'country')


### Register Models ###
admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Stakeholder, StakeholderAdmin)
admin.site.register(StakeholderType, StakeholderTypeAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(TeacherEmploymentHistory, TeacherEmploymentHistoryAdmin)  # New addition
