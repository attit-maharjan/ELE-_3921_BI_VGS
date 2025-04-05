# Generated by Django 5.1.6 on 2025-03-16 11:50

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0010_gradestream_alter_classgroup_stream'),
        ('users', '0004_remove_student_grade_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentsubjectenrollment',
            name='subject_assignment',
        ),
        migrations.RemoveField(
            model_name='studentsubjectenrollment',
            name='grade',
        ),
        migrations.AddField(
            model_name='classgroup',
            name='homeroom_teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='homeroom_classes', to='users.teacher'),
        ),
        migrations.AddField(
            model_name='classgroup',
            name='student_representative',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='representative_class', to='users.student'),
        ),
        migrations.AddField(
            model_name='studentsubjectenrollment',
            name='subject',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='academics.subject'),
        ),
        migrations.AlterField(
            model_name='classsubject',
            name='class_group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='academics.classgroup'),
        ),
        migrations.AlterField(
            model_name='classsubject',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='current_teaching_classes', to='users.teacher'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='course_code',
            field=models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator(message="Course code must be in the format 'XX-111' or 'XXXXX-11111'.", regex='^[A-Z]{2,5}-\\d{2,5}$')]),
        ),
        migrations.CreateModel(
            name='TeacherHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('reason', models.CharField(choices=[('left_temporarily', 'Left Temporarily'), ('left_permanently', 'Left Permanently'), ('deceased', 'Deceased'), ('teacher_changed', 'Teacher Changed')], max_length=255)),
                ('class_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_history', to='academics.classsubject')),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.teacher')),
            ],
        ),
        migrations.DeleteModel(
            name='SubjectAssignment',
        ),
    ]
