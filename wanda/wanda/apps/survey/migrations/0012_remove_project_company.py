# Generated by Django 4.0.6 on 2022-10-18 03:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0011_structure_alter_project_options_alter_survey_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='company',
        ),
    ]