from django.core.management.base import BaseCommand
from academics.models import AcademicYear
from datetime import date

class Command(BaseCommand):
    help = 'Loads predefined academic years into the database in decreasing order'

    def handle(self, *args, **kwargs):
        # List of years and their corresponding start and end dates
        academic_years = [
            (2025, "2025-01-01", "2025-12-31"),
            (2024, "2024-01-01", "2024-12-31"),
            (2022, "2022-01-01", "2022-12-31"),
            (2021, "2021-01-01", "2021-12-31"),
            (2020, "2020-01-01", "2020-12-31"),
            (2019, "2019-01-01", "2019-12-31"),
            (2018, "2018-01-01", "2018-12-31"),
            (2017, "2017-01-01", "2017-12-31"),
            (2016, "2016-01-01", "2016-12-31"),
        ]

        # Reversing the list to insert in decreasing order
        academic_years.reverse()

        for year, start_date, end_date in academic_years:
            # Convert string dates to date objects
            start_date_obj = date.fromisoformat(start_date)
            end_date_obj = date.fromisoformat(end_date)
            
            # Create the AcademicYear entry
            academic_year, created = AcademicYear.objects.get_or_create(
                year=year,
                start_date=start_date_obj,
                end_date=end_date_obj,
            )
            
            # Print success message
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully created academic year {year}"))
            else:
                self.stdout.write(self.style.WARNING(f"Academic year {year} already exists"))
