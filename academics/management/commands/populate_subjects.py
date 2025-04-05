from django.core.management.base import BaseCommand
from academics.models import Subject, CourseType
from django.utils.timezone import now

class Command(BaseCommand):
    help = "Populates the Subject model with predefined subjects"

    def handle(self, *args, **kwargs):
        subjects_data = [
            ("Foundations of Mathematics", "SG", "MAT-101"),
            ("Mathematics for High School", "HG", "MAT-102"),
            ("English for Communication", "SG", "ENG-101"),
            ("English Literature and Analysis", "HG", "ENG-102"),
            ("Introduction to General Science", "SG", "SCI-101"),
            ("Advanced General Science", "HG", "SCI-102"),
            ("Global Social Studies", "SG", "SOC-101"),
            ("World History & Cultures", "HG", "SOC-102"),
            ("Physical Education & Wellness", "SG", "PED-101"),
            ("Physical Education: Advanced Techniques", "HG", "PED-102"),
            ("Digital Literacy & ICT", "SG", "ICT-101"),
            ("Information Systems & Technology", "HG", "ICT-102"),
            ("Mathematical Reasoning", "SG", "MAT-201"),
            ("Advanced Mathematics", "HG", "MAT-202"),
            ("Advanced English Composition", "SG", "ENG-201"),
            ("Literary Criticism & Writing", "HG", "ENG-202"),
            ("Principles of Biology", "SG", "BIO-201"),
            ("Advanced Biology", "HG", "BIO-202"),
            ("World Geography and Cultures", "SG", "GEO-201"),
            ("Geospatial Analysis & Advanced Geography", "HG", "GEO-202"),
            ("Health & Physical Education", "SG", "PED-201"),
            ("Sports & Nutrition Science", "HG", "PED-202"),
            ("Foundations of ICT", "SG", "ICT-201"),
            ("Advanced ICT Systems", "HG", "ICT-202"),
            ("Algebra and Geometry", "SG", "MAT-301"),
            ("Advanced Algebra & Geometry", "HG", "MAT-302"),
            ("English Literature & Analysis", "SG", "ENG-301"),
            ("Comparative Literature & Interpretation", "HG", "ENG-302"),
            ("Chemistry in Action", "SG", "CHE-301"),
            ("Organic Chemistry", "HG", "CHE-302"),
            ("Modern History & Global Perspectives", "SG", "HIS-301"),
            ("World History & Philosophy", "HG", "HIS-302"),
            ("Business & Entrepreneurship", "SG", "BUS-301"),
            ("Advanced Business Management", "HG", "BUS-302"),
            ("Physical Fitness & Sports Science", "SG", "PED-301"),
            ("Sports Psychology & Performance", "HG", "PED-302"),
            ("Advanced Mathematics & Trigonometry", "SG", "MAT-401"),
            ("Calculus & Trigonometry", "HG", "MAT-402"),
            ("Creative Writing & Rhetoric", "SG", "ENG-401"),
            ("Advanced English Rhetoric", "HG", "ENG-402"),
            ("Physics: Laws of Nature", "SG", "PHY-401"),
            ("Advanced Physics: Theories", "HG", "PHY-402"),
            ("Macroeconomics & Global Trade", "SG", "ECO-401"),
            ("Global Economics & Development", "HG", "ECO-402"),
            ("Civics & Political Awareness", "SG", "POL-401"),
            ("Political Science & Global Relations", "HG", "POL-402"),
            ("Sports Science & Performance", "SG", "PED-401"),
            ("Biomechanics & Exercise Science", "HG", "PED-402"),
            ("Mathematical Models & Calculus", "SG", "MAT-501"),
            ("Advanced Calculus & Differential Equations", "HG", "MAT-502"),
            ("Advanced English: Poetry & Prose", "SG", "ENG-501"),
            ("Literary Analysis & Theory", "HG", "ENG-502"),
            ("Environmental Chemistry", "SG", "CHE-501"),
            ("Advanced Environmental Chemistry", "HG", "CHE-502"),
            ("Business Management & Marketing", "SG", "BUS-501"),
            ("International Business Strategies", "HG", "BUS-502"),
            ("Human Geography & Urban Studies", "SG", "GEO-501"),
            ("Global Urbanization & Development", "HG", "GEO-502"),
            ("Physical Education: Leadership in Sports", "SG", "PED-501"),
            ("Sport Leadership & Management", "HG", "PED-502"),
            ("ICT & Emerging Technologies", "SG", "ICT-501"),
            ("Advanced Digital Systems", "HG", "ICT-502"),
            ("Advanced Biology & Ecology", "SG", "BIO-501"),
            ("Molecular Biology & Biotechnology", "HG", "BIO-502"),
            ("Advanced Calculus & Mathematical Applications", "SG", "MAT-601"),
            ("Applied Calculus & Complex Systems", "HG", "MAT-602"),
            ("World Literature & Critical Thinking", "SG", "ENG-601"),
            ("Global Literature & Comparative Studies", "HG", "ENG-602"),
            ("Molecular Biology & Biotechnology", "SG", "BIO-601"),
            ("Advanced Molecular Genetics", "HG", "BIO-602"),
            ("Organic Chemistry & Synthesis", "SG", "CHE-601"),
            ("Advanced Organic Chemistry & Reactions", "HG", "CHE-602"),
            ("Quantum Physics & Theories", "SG", "PHY-601"),
            ("Advanced Quantum Mechanics", "HG", "PHY-602"),
            ("ICT & Emerging Technologies", "SG", "ICT-601"),
            ("Artificial Intelligence & Data Science", "HG", "ICT-602"),
            ("Advanced Sports Science & Kinesiology", "SG", "PED-601"),
            ("Sports Physiology & Performance Optimization", "HG", "PED-602"),
            ("Advanced Business & Financial Management", "SG", "BUS-601"),
            ("Global Business & Finance", "HG", "BUS-602"),
        ]

        # Sort by course number first, then alphabetically by name
        subjects_data.sort(key=lambda x: (int(x[2].split('-')[1]), x[0]))

        subjects_created = 0
        for name, course_type_abbr, course_code in subjects_data:
            course_type = CourseType.objects.filter(abbreviation=course_type_abbr).first()
            if not course_type:
                self.stdout.write(self.style.ERROR(f"Skipping '{name}': Course type '{course_type_abbr}' not found."))
                continue

            subject, created = Subject.objects.update_or_create(
                course_code=course_code,
                defaults={
                    "name": name,
                    "course_type": course_type,
                    "date_registered": now(),
                    "is_active": True
                }
            )
            if created:
                subjects_created += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully added {subjects_created} subjects."))
