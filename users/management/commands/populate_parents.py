import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_date
from users.models import User, Parent, Address
from django.conf import settings


class Command(BaseCommand):
    help = "Import parents from a CSV file and create user accounts."

    def handle(self, *args, **kwargs):
        csv_file = settings.BASE_DIR / 'data' / 'csv' / 'parent.csv'

        if not csv_file.exists():
            self.stderr.write(self.style.ERROR(f"File not found: {csv_file}"))
            return

        with open(csv_file, newline='', encoding='ISO-8859-1') as file:
            reader = csv.DictReader(file)

            for row in reader:
                email = row['email'].strip()
                first_name = row['fNAME'].strip()
                last_name = row['lNAME'].strip()
                gender = row['gender'].strip().lower()
                phone_number = row['phone_number'].strip()
                password1 = row['password1'].strip()
                password2 = row['password2'].strip()
                relationship = row['Relationship'].strip()

                # Ensure passwords match
                if password1 != password2:
                    self.stderr.write(self.style.ERROR(f"Skipping {email}: Passwords do not match."))
                    continue

                # Handle address
                address, created = Address.objects.get_or_create(
                    street_address=row['street_address'].strip(),
                    city=row['city'].strip(),
                    state_province=row.get('state_province', '').strip(),
                    postal_code=row.get('postal_code', '').strip(),
                    country=row['country'].strip()
                )

                # Create User
                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={
                        'first_name': first_name,
                        'last_name': last_name,
                        'phone_number': phone_number,
                        'role': 'parent',
                        'address': address,
                    }
                )

                if created:
                    user.set_password(password1)
                    user.save()
                    self.stdout.write(self.style.SUCCESS(f"User created: {email}"))

                    # Create Parent record
                    Parent.objects.create(
                        user=user,
                        relationship_to_student=relationship
                    )
                    self.stdout.write(self.style.SUCCESS(f"Parent created: {email}"))

                else:
                    self.stdout.write(self.style.WARNING(f"User already exists: {email}"))
