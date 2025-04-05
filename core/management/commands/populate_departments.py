from django.core.management.base import BaseCommand
from users.models import Department  # Replace 'your_app' with your actual app name

class Command(BaseCommand):
    help = "Populates the Department model with common high school departments."

    def handle(self, *args, **kwargs):
        departments = [
            {"name": "English / Language Arts", "description": "Covers literature, writing, and communication skills."},
            {"name": "Mathematics", "description": "Includes algebra, geometry, trigonometry, and calculus."},
            {"name": "Science", "description": "Covers biology, chemistry, physics, and earth science."},
            {"name": "Social Studies / History", "description": "Includes history, geography, government, and economics."},
            {"name": "Foreign Languages", "description": "Covers languages such as Spanish, French, German, and more."},
            {"name": "Computer Science / IT", "description": "Focuses on coding, networks, and cybersecurity."},
            {"name": "Engineering & Robotics", "description": "Teaches engineering principles and robotics."},
            {"name": "Environmental Science", "description": "Covers ecosystems, sustainability, and climate studies."},
            {"name": "Visual Arts", "description": "Includes painting, drawing, sculpture, and photography."},
            {"name": "Performing Arts", "description": "Covers music, theater, and dance."},
            {"name": "Creative Writing & Journalism", "description": "Focuses on storytelling, news writing, and media."},
            {"name": "Philosophy & Ethics", "description": "Covers critical thinking, logic, and moral philosophy."},
            {"name": "Business & Entrepreneurship", "description": "Includes business management, startups, and economics."},
            {"name": "Marketing & Finance", "description": "Covers financial literacy, marketing strategies, and economics."},
            {"name": "Automotive Technology", "description": "Focuses on vehicle mechanics and maintenance."},
            {"name": "Construction & Woodworking", "description": "Teaches carpentry, design, and construction."},
            {"name": "Culinary Arts & Hospitality", "description": "Includes cooking, baking, and restaurant management."},
            {"name": "Health Sciences / Pre-Nursing", "description": "Covers medical studies, nursing, and first aid."},
            {"name": "Agriculture & Veterinary Science", "description": "Focuses on farming, animals, and sustainability."},
            {"name": "Physical Education (PE) & Sports", "description": "Includes fitness, sports, and wellness."},
            {"name": "Health & Nutrition", "description": "Covers healthy living, diet, and well-being."},
            {"name": "Psychology & Counseling", "description": "Teaches mental health, behavior, and therapy basics."},
            {"name": "Special Education", "description": "Supports students with learning differences and disabilities."},
            {"name": "Library & Media Studies", "description": "Covers research skills, digital literacy, and library science."},
            {"name": "Religious Studies / Ethics", "description": "Teaches world religions, moral values, and theology."},
            {"name": "Military Science (ROTC)", "description": "Focuses on leadership, discipline, and military training."},
        ]

        for dept in departments:
            obj, created = Department.objects.get_or_create(name=dept["name"], defaults={"description": dept["description"]})
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added department: {dept['name']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Department already exists: {dept['name']}"))

        self.stdout.write(self.style.SUCCESS("Department population complete!"))
