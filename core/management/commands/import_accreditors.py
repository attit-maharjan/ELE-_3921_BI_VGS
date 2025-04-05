import csv
import os
from django.core.management.base import BaseCommand
from core.models import Accreditor  # Ensure this matches your app name

class Command(BaseCommand):
    help = "Import accreditors from a CSV file."

    def handle(self, *args, **kwargs):
        csv_file_path = os.path.join("core", "data", "accreditors.csv")  # Updated path

        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {csv_file_path}"))
            return

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0

            for row in reader:
                accreditor, created = Accreditor.objects.get_or_create(
                    name=row["name"],
                    registration_number=row["registration_number"],
                    defaults={
                        "website": row["website"],
                        "accreditation_date": row["accreditation_date"],
                        "status": row["status"],
                    },
                )

                if created:
                    count += 1
                    self.stdout.write(self.style.SUCCESS(f"Added: {accreditor.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Skipped (already exists): {accreditor.name}"))

        self.stdout.write(self.style.SUCCESS(f"Import completed: {count} new accreditors added."))
