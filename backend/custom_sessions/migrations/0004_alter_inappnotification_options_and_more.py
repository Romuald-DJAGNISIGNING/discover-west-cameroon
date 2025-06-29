# Generated by Django 5.2 on 2025-06-27 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_sessions', '0003_customsession_can_communicate_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inappnotification',
            options={'ordering': ['-created_at'], 'verbose_name': 'In-App Notification', 'verbose_name_plural': 'In-App Notifications'},
        ),
        migrations.AlterModelOptions(
            name='sessionfeedback',
            options={'ordering': ['-created_at'], 'verbose_name': 'Session Feedback', 'verbose_name_plural': 'Session Feedbacks'},
        ),
        migrations.AlterModelOptions(
            name='sessionmaterial',
            options={'ordering': ['-uploaded_at'], 'verbose_name': 'Session Material', 'verbose_name_plural': 'Session Materials'},
        ),
    ]
