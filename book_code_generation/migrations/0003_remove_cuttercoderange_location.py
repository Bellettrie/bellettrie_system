# Generated by Django 3.0.4 on 2020-09-23 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book_code_generation', '0002_cuttercoderange_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuttercoderange',
            name='location',
        ),
    ]
