# Generated by Django 3.0.4 on 2020-08-18 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_pages', '0002_publicpage_custom_header'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='root/uploads/')),
            ],
        ),
    ]