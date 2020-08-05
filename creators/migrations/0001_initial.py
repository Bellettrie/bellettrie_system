# Generated by Django 3.0.4 on 2020-08-05 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CreatorRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Creator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('given_names', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('comment', models.CharField(max_length=255)),
                ('old_id', models.IntegerField()),
                ('identifying_code', models.CharField(max_length=16, null=True)),
                ('is_alias_of', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='creators.Creator')),
            ],
        ),
    ]
