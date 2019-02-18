# Generated by Django 2.1.1 on 2018-12-07 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TimelineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delete_flag', models.BooleanField(default=False, verbose_name='是否被删除')),
                ('delete_time', models.DateTimeField(blank=True, null=True, verbose_name='删除时间')),
                ('open_code', models.CharField(blank=True, max_length=32, null=True, unique=True)),
                ('date', models.DateField()),
                ('title', models.CharField(default='', max_length=128)),
                ('content', models.CharField(default='', max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TimelineLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delete_flag', models.BooleanField(default=False, verbose_name='是否被删除')),
                ('delete_time', models.DateTimeField(blank=True, null=True, verbose_name='删除时间')),
                ('open_code', models.CharField(blank=True, max_length=32, null=True, unique=True)),
                ('year', models.PositiveSmallIntegerField()),
                ('title', models.CharField(default='', max_length=128)),
                ('content', models.CharField(default='', max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='timelineitem',
            name='timeline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='timeline_items', to='timeline.TimelineLine'),
        ),
    ]