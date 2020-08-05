# Generated by Django 3.0.4 on 2020-08-03 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0004_auto_20200731_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='book_code_sortable',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='publication',
            name='book_code_sortable',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='item',
            name='book_code',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='publication',
            name='book_code',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]