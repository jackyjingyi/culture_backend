# Generated by Django 4.0.6 on 2022-07-29 02:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_option_page_single'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='single',
            name='items',
        ),
        migrations.RemoveField(
            model_name='single',
            name='page',
        ),
        migrations.RemoveField(
            model_name='single',
            name='survey',
        ),
        migrations.DeleteModel(
            name='Option',
        ),
        migrations.DeleteModel(
            name='Single',
        ),
    ]
