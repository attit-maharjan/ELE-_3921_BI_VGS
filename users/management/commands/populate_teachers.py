import csv
from django.core.management.base import BaseCommand
from users.models import User, Teacher
from django.db import IntegrityError
from datetime import datetime

class Command(BaseCommand):
    help = 'Load teachers from a CSV file and create users and teachers'

    def handle(self, *args, **kwargs):
        csv_file_path = 'data/csv/teacher.csv'

        # Open the CSV file
        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                email = row['email']
                first_name = row['fname']
                last_name = row['lname']
                role = row['role']
                password = row['password1']
                phone_number = row['phone_number']
                hire_date_str = row['hireDate']

                # Convert hireDate to a datetime object
                try:
                    hire_date = datetime.strptime(hire_date_str, '%Y-%m-%d').date()
                except ValueError:
                    self.stdout.write(self.style.ERROR(f"Invalid hire date format for {first_name} {last_name}. Expected format: YYYY-MM-DD"))
                    continue

                try:
                    # Create User object
                    user = User.objects.create_user(
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        role=role,
                        password=password,
                        phone_number=phone_number  # Assuming phone_number is a field in User model
                    )

                    # Create Teacher object
                    teacher = Teacher.objects.create(
                        user=user,
                        salary=50000.00,  # You can set this value to something appropriate
                        hire_date=hire_date
                    )

                    # Optionally, set departments and subjects based on your use case
                    # For example, if you have a specific subject or department
                    # teacher.departments.add(Department.objects.get(name="Math"))
                    # teacher.subject_specialization.add(Subject.objects.get(name="Math"))

                    self.stdout.write(self.style.SUCCESS(f"Successfully added teacher: {first_name} {last_name}"))

                except IntegrityError as e:
                    self.stdout.write(self.style.ERROR(f"Error adding teacher {first_name} {last_name}: {e}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Unexpected error: {e}"))
