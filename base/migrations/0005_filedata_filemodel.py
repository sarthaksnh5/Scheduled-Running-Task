# Generated by Django 3.2.9 on 2022-04-25 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0004_delete_filemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileCount', models.CharField(max_length=200)),
                ('looping', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='FileData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startTime', models.TimeField()),
                ('endTime', models.TimeField()),
                ('sequence', models.CharField(max_length=2)),
                ('date', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to='media/')),
                ('fileModel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.filemodel')),
            ],
        ),
    ]
