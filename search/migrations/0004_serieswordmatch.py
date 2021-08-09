# Generated by Django 3.1.5 on 2021-08-01 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0004_series_location_code'),
        ('search', '0003_auto_20210801_1319'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeriesWordMatch',
            fields=[
                ('wordmatch_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='search.wordmatch')),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='series.series')),
            ],
            bases=('search.wordmatch',),
        ),
    ]