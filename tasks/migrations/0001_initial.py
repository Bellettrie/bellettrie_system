# Generated by Django 4.2.15 on 2024-09-23 07:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=100)),
                ('object_as_json', models.TextField()),
                ('next_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('done', models.BooleanField(default=False)),
                ('repeats_every_minutes', models.IntegerField(default=0, verbose_name='frequency (in minutes) of execution of task')),
            ],
        ),
    ]