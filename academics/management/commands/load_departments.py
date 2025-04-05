from django.core.management.base import BaseCommand
from academics.models import Department

class Command(BaseCommand):
    help = "Populates the Department model with predefined departments."

    def handle(self, *args, **kwargs):
        departments = [
            {"code": "MAT", "name": "Mathematics", "description": "Includes algebra, geometry, trigonometry, and calculus."},
            {"code": "SCI", "name": "Science", "description": "Covers biology, chemistry, physics, and earth science."},
            {"code": "ENG", "name": "English / Language Arts", "description": "Covers literature, writing, and communication skills."},
            {"code": "SOC", "name": "Social Studies / History", "description": "Includes history, geography, government, and economics."},
            {"code": "FLN", "name": "Foreign Languages", "description": "Covers languages such as Spanish, French, German, and more."},
            {"code": "CSC", "name": "Computer Science / IT", "description": "Focuses on coding, networks, and cybersecurity."},
            {"code": "EGR", "name": "Engineering & Robotics", "description": "Teaches engineering principles and robotics."},
            {"code": "ENV", "name": "Environmental Science", "description": "Covers ecosystems, sustainability, and climate studies."},
            {"code": "ART", "name": "Visual Arts", "description": "Includes painting, drawing, sculpture, and photography."},
            {"code": "PER", "name": "Performing Arts", "description": "Covers music, theater, and dance."},
            {"code": "CWJ", "name": "Creative Writing & Journalism", "description": "Focuses on storytelling, news writing, and media."},
            {"code": "PHE", "name": "Physical Education (PE) & Sports", "description": "Includes fitness, sports, and wellness."},
            {"code": "HEA", "name": "Health Sciences / Pre-Nursing", "description": "Covers medical studies, nursing, and first aid."},
            {"code": "HNU", "name": "Health & Nutrition", "description": "Covers healthy living, diet, and well-being."},
            {"code": "AGR", "name": "Agriculture & Veterinary Science", "description": "Focuses on farming, animals, and sustainability."},
            {"code": "CUL", "name": "Culinary Arts & Hospitality", "description": "Includes cooking, baking, and restaurant management."},
            {"code": "BUS", "name": "Business & Entrepreneurship", "description": "Includes business management, startups, and economics."},
            {"code": "MAR", "name": "Marketing & Finance", "description": "Covers financial literacy, marketing strategies, and economics."},
            {"code": "AUT", "name": "Automotive Technology", "description": "Focuses on vehicle mechanics and maintenance."},
            {"code": "CON", "name": "Construction & Woodworking", "description": "Teaches carpentry, design, and construction."},
        ]

        count = 0
        for dept in departments:
            _, created = Department.objects.get_or_create(
                code=dept["code"],
                defaults={"name": dept["name"], "description": dept["description"]}
            )
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully added {count} departments."))
