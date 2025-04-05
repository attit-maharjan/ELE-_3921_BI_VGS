import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from academics.models import GradeLevel

class Command(BaseCommand):
    help = "Populate the GradeLevel model from a CSV file"

    def handle(self, *args, **kwargs):
        csv_file_path = os.path.join(settings.CSV_DATA_DIR, "populate_grades.csv")

        if not os.path.isfile(csv_file_path):
            self.stderr.write(self.style.ERROR(f"CSV file not found: {csv_file_path}"))
            return

        try:
            with open(csv_file_path, mode="r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)

                created_count = 0
                updated_count = 0

                for row in reader:
                    name = row["name"].strip()
                    numeric_level = int(row["numeric_level"])
                    description = row["description"].strip()

                    grade, created = GradeLevel.objects.update_or_create(
                        numeric_level=numeric_level,
                        defaults={"name": name, "description": description}
                    )

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

            self.stdout.write(self.style.SUCCESS(
                f"Population complete! {created_count} new grades added, {updated_count} existing grades updated."
            ))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error processing file: {e}"))
