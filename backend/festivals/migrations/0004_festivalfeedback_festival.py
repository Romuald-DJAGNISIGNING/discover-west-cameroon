# Generated by Django 5.2 on 2025-06-27 13:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('festivals', '0003_alter_festival_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='festivalfeedback',
            name='festival',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='festivals.festival'),
        ),
    ]
