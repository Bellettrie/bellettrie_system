# Generated by Django 3.0.4 on 2020-08-18 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_pages', '0003_fileupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileupload',
            name='name',
            field=models.CharField(default='a', max_length=64),
            preserve_default=False,
        ),
    ]
