from django.urls import path
from core import views


# Set the application namespace to 'core'.
# This is necessary for namespacing URL names in templates and views.
app_name = 'core'  

urlpatterns = [
    # URL pattern for the homepage, mapped to the `index` view.
    path('', views.index, name='index'),

    # URL pattern for the "About" page, mapped to the `about` view.
    path('about/', views.about, name='about'),

    # URL pattern for the "Contact" page, mapped to the `contact` view.
    path('contact/', views.contact, name='contact'),

    # URL pattern for the "Academics" page, mapped to the `academics` view.
    path('academics/', views.academics, name='academics'),  

    # URL pattern for the "Admissions" page, mapped to the `admissions` view.
    path('admissions/', views.admissions, name='admissions'),

    # URL pattern for the "User Login" page, mapped to the `user_login` view.
    path('login/', views.user_login, name='login'),

    # URL pattern for the "Student Login" page, mapped to the `student_login` view.
    path('student_login/', views.student_login, name='student_login'),  

    # URL pattern for the "Teacher Login" page, mapped to the `teacher_login` view.
    path('teacher_login/', views.teacher_login, name='teacher_login'),  
    
    # URL pattern for the "Parent Login" page, mapped to the `parent_login` view.
    path('parent_login/', views.parent_login, name='parent_login'),

    
    # URL pattern for the "Admin Login" page, mapped to the `admin_login` view.
    path('admin_login/', views.admin_login, name='admin_login'),

    # URL pattern for the "Stakeholder Login" page, mapped to the `stakeholder_login` view.
    path('stakeholder_login/', views.stakeholder_login, name='stakeholder_login'),

    # URL pattern for the "Staff Login" page, mapped to the `staff_login` view.
    path('staff_login/', views.staff_login, name='staff_login'),

    # URL pattern for the "Student Dashboard" page, mapped to the `student_dashboard` view.
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),

    # URL pattern for the "Teacher Dashboard" page, mapped to the `teacher_dashboard` view.
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    # URL pattern for the "Parent Dashboard" page, mapped to the `parent_dashboard` view.
    path('parent_dashboard/', views.parent_dashboard, name='parent_dashboard'), 

    # URL pattern for the "Admin Dashboard" page, mapped to the `admin_dashboard` view.
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # URL pattern for the "Stakeholder Dashboard" page, mapped to the `stakeholder_dashboard` view.
    path('stakeholder_dashboard/', views.stakeholder_dashboard, name='stakeholder_dashboard'),

    # URL pattern for the "Staff Dashboard" page, mapped to the `staff_dashboard` view.
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),

    path ('logout/', views.logout_view, name='logout'),
]
