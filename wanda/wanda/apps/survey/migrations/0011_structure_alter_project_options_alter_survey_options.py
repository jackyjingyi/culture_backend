# Generated by Django 4.0.6 on 2022-10-18 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0010_alter_blank_qtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Structure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-created_dt'], 'permissions': [('create_survey', '创建问卷')]},
        ),
        migrations.AlterModelOptions(
            name='survey',
            options={'permissions': [('publish_survey', '发布权限'), ('invite_user', '邀请编辑')]},
        ),
    ]
