# Generated by Django 5.2 on 2025-06-06 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorial',
            name='language',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
