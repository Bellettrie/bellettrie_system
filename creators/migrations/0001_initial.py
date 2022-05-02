# Generated by Django 3.2.10 on 2022-05-02 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Creator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('given_names', models.CharField(blank=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('comment', models.CharField(max_length=255)),
                ('old_id', models.IntegerField(blank=True, null=True)),
                ('mark_for_change', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CreatorRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='LocationNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('letter', models.CharField(max_length=16)),
                ('name', models.CharField(blank=True, max_length=64, null=True)),
                ('auto_name', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='CreatorLocationNumber',
            fields=[
                ('locationnumber_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='creators.locationnumber')),
            ],
            bases=('creators.locationnumber',),
        ),
    ]
