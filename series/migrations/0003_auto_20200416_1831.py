# Generated by Django 3.0.4 on 2020-04-16 18:31

from django.db import migrations

from works.management.commands.destroy_problems import destroy_problems


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0002_auto_20200416_1830'),
    ]

    operations = [
        migrations.RunPython(destroy_problems),
        migrations.AlterUniqueTogether(
            name='seriesnode',
            unique_together={('number', 'part_of_series')},
        ),
    ]
