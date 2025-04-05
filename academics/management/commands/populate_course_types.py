from django.core.management.base import BaseCommand
from academics.models import CourseType

class Command(BaseCommand):
    help = "Populates the database with default Course Types if they don't exist"

    COURSE_TYPES = [
        {"name": "Standard Grade", "abbreviation": "SG", "description": "Basic level of the course, suitable for general learners."},
        {"name": "Higher Grade", "abbreviation": "HG", "description": "Advanced level of the course, covering more depth."},
        {"name": "Elective", "abbreviation": "ELEC", "description": "Optional courses chosen by students based on interest."},
        {"name": "Core", "abbreviation": "CORE", "description": "Mandatory courses required for the curriculum."},
        {"name": "Honors", "abbreviation": "HON", "description": "Courses designed for high-achieving students with deeper content."},
        {"name": "Remedial", "abbreviation": "REM", "description": "Courses designed for students needing additional academic support."},
        {"name": "Advanced Placement", "abbreviation": "AP", "description": "College-level courses for high school students."},
        {"name": "International Baccalaureate", "abbreviation": "IB", "description": "Courses based on the IB curriculum framework."},
        {"name": "Technical", "abbreviation": "TECH", "description": "Courses focused on vocational and technical skills."},
        {"name": "Online", "abbreviation": "ONLINE", "description": "Courses offered through digital platforms."},
        {"name": "Hybrid", "abbreviation": "HYB", "description": "Courses combining online and in-person instruction."},
        {"name": "Short Course", "abbreviation": "SC", "description": "Short-term intensive courses on specific topics."},
        {"name": "Workshop", "abbreviation": "WS", "description": "Practical, hands-on courses focused on skill-building."},
    ]

    def handle(self, *args, **kwargs):
        created_count = 0
        for course in self.COURSE_TYPES:
            obj, created = CourseType.objects.get_or_create(
                name=course["name"],
                defaults={"abbreviation": course["abbreviation"], "description": course["description"], "is_active": True},
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Added CourseType: {obj.abbreviation} - {obj.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'CourseType already exists: {obj.abbreviation} - {obj.name}'))

        self.stdout.write(self.style.SUCCESS(f'Total new CourseTypes added: {created_count}'))
