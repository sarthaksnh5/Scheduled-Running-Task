# Generated by Django 3.2.9 on 2022-04-25 04:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20220425_0933'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FileData',
        ),
        migrations.DeleteModel(
            name='FileModel',
        ),
    ]
