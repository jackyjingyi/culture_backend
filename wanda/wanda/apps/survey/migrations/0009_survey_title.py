# Generated by Django 4.0.6 on 2022-07-30 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0008_page_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='title',
            field=models.CharField(default='test', max_length=255, verbose_name='项目标题'),
            preserve_default=False,
        ),
    ]