# Generated by Django 5.1.6 on 2025-03-16 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_stakeholdertype_remove_stakeholder_stakeholder_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='grade_level',
        ),
    ]
