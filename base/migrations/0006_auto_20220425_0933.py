# Generated by Django 3.2.9 on 2022-04-25 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_filedata_filemodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filedata',
            name='sequence',
            field=models.CharField(default=1, max_length=2),
        ),
        migrations.AlterField(
            model_name='filemodel',
            name='looping',
            field=models.CharField(default=1, max_length=3),
        ),
    ]
