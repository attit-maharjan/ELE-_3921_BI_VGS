import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from users.models import Teacher, User

class Command(BaseCommand):
    help = 'Bulk load teachers into the system'

    def handle(self, *args, **kwargs):
        # Get the absolute path to the CSV file in the static directory
        csv_path = os.path.join(settings.BASE_DIR, 'static', 'teachers.csv')

        # Ensure the file exists before trying to open it
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f"CSV file not found: {csv_path}"))
            return

        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Create User
                user = User.objects.create_user(
                    username=row['email'], 
                    email=row['email'],
                    password='defaultpassword123',  # Consider using a default password
                    role='teacher'
                )
                
                # Create Teacher
                Teacher.objects.create(
                    user=user,
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    dob=row['dob'],
                    gender=row['gender'],
                    email=row['email'],
                    subject_specialization=row['subject_specialization'],
                    employment_type=row['employment_type'],
                    salary=row['salary']
                )
            self.stdout.write(self.style.SUCCESS('Successfully bulk loaded teachers'))
