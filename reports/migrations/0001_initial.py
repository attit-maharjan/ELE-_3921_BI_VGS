# Generated by Django 5.1.6 on 2025-03-13 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback_date', models.DateField()),
                ('feedback_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ReportCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_results', models.JSONField()),
                ('overall_grade', models.CharField(max_length=10)),
                ('report_generated_date', models.DateField()),
            ],
        ),
    ]
