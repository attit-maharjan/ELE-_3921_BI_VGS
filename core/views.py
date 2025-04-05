from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from communications.models import Announcement
from core.models import SchoolSettings, Accreditor
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
import json
from users.models import User  # Import the custom User model from the 'users' app

# View function for the homepage.
# This function renders the 'core/index.html' template when the home page is accessed.
def index(request):
    """Fetch the five most recent active announcements"""
    recent_announcements = Announcement.objects.filter(status='active').order_by('-created_at')[:5]
    return render(request, 'core/index.html', {'recent_announcements': recent_announcements})
   

# View function for the "About" page.
# This function renders the 'core/about.html' template when the about page is accessed.
def about(request):
    return render(request, 'core/about.html')

# View function for the "Contact" page.
# This function renders the 'core/contact.html' template when the contact page is accessed.
def contact(request):
    return render(request, 'core/contact.html')

def academics(request):
    return render(request, 'core/academics.html')

def admissions(request):
    return render(request, 'core/admissions.html')

def user_login(request):  
    return render(request, 'core/login.html')

def student_login(request):
    if request.method == 'POST':
        student_email = request.POST.get('username')  # Email is used as the username
        password = request.POST.get('password')
        print(f"Attempting login for email: {student_email}")  # Debug print

        # Authenticate using email and password
        user = authenticate(request, username=student_email, password=password)  # Authenticate using email
        if user is not None:
            print("Authentication successful")  # Debug print
            login(request, user)  # This now correctly calls Django's auth.login
            return redirect('core:student_dashboard')  # Redirect to student dashboard
        else:
            print("Authentication failed")  # Debug print
            return render(request, 'core/student_login.html', {'error': 'Invalid email or password'})
    return render(request, 'core/student_login.html')

def teacher_login(request):
    if request.method == 'POST':
        email = request.POST.get('username')  # Email is used as the username
        password = request.POST.get('password')
        user = User.objects.filter(email=email).first()  # Find user by email
        if user:
            user = authenticate(request, username=user.username, password=password)  # Authenticate using username
            if user is not None:
                login(request, user)
                return redirect('core:teacher_dashboard')  # Redirect to teacher dashboard
        return render(request, 'core/teacher_login.html', {'error': 'Invalid email or password'})
    return render(request, 'core/teacher_login.html')

def parent_login(request):
    if request.method == 'POST':
        email = request.POST.get('username')  # Email is used as the username
        password = request.POST.get('password')
        user = User.objects.filter(email=email).first()  # Find user by email
        if user:
            user = authenticate(request, username=user.username, password=password)  # Authenticate using username
            if user is not None:
                login(request, user)
                return redirect('core:parent_dashboard')  # Redirect to parent dashboard
        return render(request, 'core/parent_login.html', {'error': 'Invalid email or password'})
    return render(request, 'core/parent_login.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('core/admin_dashboard')  # Redirect to the admin dashboard
        else:
            return render(request, 'core/admin_login.html', {'error': 'Invalid username or password'})
    return render(request, 'core/admin_login.html')

def stakeholder_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('core/stakeholder_dashboard')  # Redirect to the stakeholder dashboard
        else:
            return render(request, 'core/stakeholder_login.html', {'error': 'Invalid username or password'})
    return render(request, 'core/stakeholder_login.html')

def staff_login(request):
    if request.method == 'POST':
        email = request.POST.get('username')  # Email is used as the username
        password = request.POST.get('password')
        user = User.objects.filter(email=email).first()  # Find user by email
        if user:
            user = authenticate(request, username=user.username, password=password)  # Authenticate using username
            if user is not None:
                login(request, user)
                return redirect('staff_dashboard')  # Redirect to staff dashboard
        return render(request, 'core/staff_login.html', {'error': 'Invalid email or password'})
    return render(request, 'core/staff_login.html')

@login_required
def student_dashboard(request):
    # Example data for the dashboard
    schedule = [
        {'day': 'Monday', 'classes': [{'time': '9:00 AM', 'subject': 'Math', 'room': '101'}, {'time': '11:00 AM', 'subject': 'Science', 'room': '102'}]},
        {'day': 'Tuesday', 'classes': [{'time': '10:00 AM', 'subject': 'English', 'room': '103'}, {'time': '1:00 PM', 'subject': 'History', 'room': '104'}]},
    ]

    assignments = [
        {'id': 1, 'subject': 'Math', 'description': 'Complete Chapter 5', 'due_date': '2025-04-10', 'submitted': False},
        {'id': 2, 'subject': 'Science', 'description': 'Lab Report on Experiment 3', 'due_date': '2025-04-12', 'submitted': True, 'submission_date': '2025-04-08'},
    ]

    results = [
        {'subject': 'Math', 'marks': 95, 'grade': 'A', 'rank': 1},
        {'subject': 'Science', 'marks': 88, 'grade': 'B+', 'rank': 3},
        {'subject': 'English', 'marks': 92, 'grade': 'A-', 'rank': 2},
    ]

    context = {
        'user': request.user,
        'school_settings': SchoolSettings.objects.first(),  # Assuming you have a SchoolSettings model
        'student_class': '10th Grade',  # Example data
        'enrollment_number': request.user.email,  # Use the email as enrollment number
        'schedule': schedule,
        'assignments': assignments,
        'results': results,
    }

    return render(request, 'core/dashboards/student_dashboard.html', context)

def teacher_dashboard(request):
    # Example dashboard view
    return render(request, 'core/teacher_dashboard.html')

def parent_dashboard(request):
    return render(request, 'core/parent_dashboard.html')

def admin_dashboard(request):
    return render(request, 'core/admin_dashboard.html')

def stakeholder_dashboard(request):
    total_students = 100  # Example value
    total_staff = 20  # Example value
    subject_list = ['Math', 'Science', 'English']  # Example list
    attendance_list = [80, 90, 85]  # Example list

    context = {
        'total_students': total_students,
        'total_staff': total_staff,
        'subject_list': mark_safe(json.dumps(subject_list)),
        'attendance_list': mark_safe(json.dumps(attendance_list)),
        'page_title': 'Stakeholder Dashboard',
        'chart_js': '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>'
    }
    return render(request, 'core/stakeholder_dashboard.html', context)

def staff_dashboard(request):
    return render(request, 'core/staff_dashboard.html')


def logout_view(request):
    """Logs out the user and redirects to the homepage."""
    logout(request)
    return redirect('core:index')  # Redirect to the homepage after logout

