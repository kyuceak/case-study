# Generated by Django 5.1.4 on 2024-12-21 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0007_rename_aircraft_part_aircraft_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='responsible',
        ),
    ]