# Generated by Django 2.1.1 on 2018-12-09 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slideshow',
            name='title',
            field=models.CharField(default='', max_length=64),
        ),
    ]
