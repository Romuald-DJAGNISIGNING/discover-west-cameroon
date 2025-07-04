# Generated by Django 5.2 on 2025-06-26 11:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='assignment_type',
            field=models.CharField(choices=[('tutoring', 'Tutoring'), ('tour', 'Tour Guide')], default='tutoring', max_length=16, verbose_name='Assignment Type'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='assignments/attachments/', verbose_name='Attachment (optional)'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='external_link',
            field=models.URLField(blank=True, null=True, verbose_name='External Link (optional)'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is Active'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated At'),
        ),
        migrations.AddField(
            model_name='assignmentsubmission',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Submission Comment'),
        ),
        migrations.AddField(
            model_name='assignmentsubmission',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='assigned_by',
            field=models.ForeignKey(help_text='The tutor or guide who creates this assignment.', on_delete=django.db.models.deletion.CASCADE, related_name='assignments_given', to=settings.AUTH_USER_MODEL, verbose_name='Assigned By'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='assigned_to',
            field=models.ForeignKey(help_text='The learner who receives this assignment.', on_delete=django.db.models.deletion.CASCADE, related_name='assignments_received', to=settings.AUTH_USER_MODEL, verbose_name='Assigned To'),
        ),
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='student',
            field=models.ForeignKey(help_text='The learner submitting.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Learner'),
        ),
        migrations.AlterUniqueTogether(
            name='assignmentsubmission',
            unique_together={('assignment', 'student')},
        ),
    ]
