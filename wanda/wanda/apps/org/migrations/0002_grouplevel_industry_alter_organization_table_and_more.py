# Generated by Django 4.0.6 on 2022-10-25 06:58

from django.db import migrations, models
import django.db.models.deletion
import wanda.apps.org.models


class Migration(migrations.Migration):

    dependencies = [
        ('org', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupLevel',
            fields=[
                ('group_level_id', models.CharField(default=wanda.apps.org.models.nanoid_generate, max_length=25, primary_key=True, serialize=False, verbose_name='组ID')),
                ('group_level_name', models.CharField(max_length=15, verbose_name='分组名称')),
                ('level_children_id', models.CharField(blank=True, max_length=25, null=True, verbose_name='子等级ID')),
                ('level_num', models.IntegerField(default=0, help_text='顺序自增', verbose_name='等级')),
                ('version_id', models.IntegerField(default=0, verbose_name='版本')),
            ],
            options={
                'db_table': 'GroupLevel',
            },
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.CharField(default=wanda.apps.org.models.nanoid_generate, max_length=25, primary_key=True, serialize=False, verbose_name='行业ID')),
                ('name', models.CharField(max_length=20, verbose_name='行业名称')),
                ('code', models.IntegerField(verbose_name='行业代码')),
            ],
            options={
                'db_table': 'Industry',
            },
        ),
        migrations.AlterModelTable(
            name='organization',
            table='Organization',
        ),
        migrations.CreateModel(
            name='OrgGroup',
            fields=[
                ('id', models.CharField(default=wanda.apps.org.models.nanoid_generate, max_length=25, primary_key=True, serialize=False, verbose_name='组ID')),
                ('group_name', models.CharField(max_length=20, verbose_name='名称')),
                ('group_code', models.CharField(max_length=20, verbose_name='组代码')),
                ('group_status', models.IntegerField(default=0, verbose_name='状态')),
                ('have_children', models.BooleanField(default=False)),
                ('leaf_flag', models.BooleanField(default=True)),
                ('group_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.grouplevel')),
                ('group_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', related_query_name='child', to='org.orggroup')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.organization')),
            ],
            options={
                'db_table': 'OrgGroup',
            },
        ),
        migrations.AddField(
            model_name='grouplevel',
            name='org',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.organization'),
        ),
        migrations.AddField(
            model_name='organization',
            name='industry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='org.industry'),
        ),
    ]