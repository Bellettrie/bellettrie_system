# Generated by Django 3.0.4 on 2020-09-13 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creators', '0002_creatorlocationnumber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creator',
            name='identifying_code',
        ),
        migrations.AddField(
            model_name='creatorlocationnumber',
            name='letter',
            field=models.CharField(default=1, max_length=16),
            preserve_default=False,
        ),
    ]