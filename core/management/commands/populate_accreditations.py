import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Accreditor  # Ensure your model is correctly imported

class Command(BaseCommand):
    help = "Populate the Accreditor model from a CSV file."

    def handle(self, *args, **kwargs):
        csv_file_path = os.path.join(settings.CSV_DATA_DIR, 'populate_accreditation.csv')
        
        if not os.path.exists(csv_file_path):
            self.stderr.write(self.style.ERROR(f"CSV file not found: {csv_file_path}"))
            return
        
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                accreditor, created = Accreditor.objects.update_or_create(
                    registration_number=row['registration_number'],
                    defaults={
                        'name': row['name'],
                        'website': row['website'] if row['website'] else None,
                        'accreditation_date': row['accreditation_date'],
                        'status': row['status'],
                    }
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Added: {accreditor.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Updated: {accreditor.name}"))
