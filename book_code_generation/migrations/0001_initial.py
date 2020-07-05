# Generated by Django 3.0.4 on 2020-07-05 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CutterCodeRange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_affix', models.CharField(max_length=16)),
                ('to_affix', models.CharField(max_length=16)),
                ('number', models.CharField(max_length=16)),
                ('generated_affix', models.CharField(max_length=20)),
            ],
        ),
    ]
