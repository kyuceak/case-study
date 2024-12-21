# Generated by Django 5.1.4 on 2024-12-21 12:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0006_team_responsible'),
    ]

    operations = [
        migrations.RenameField(
            model_name='part',
            old_name='aircraft',
            new_name='aircraft_type',
        ),
        migrations.RemoveField(
            model_name='aircraft',
            name='avionics',
        ),
        migrations.RemoveField(
            model_name='aircraft',
            name='fuselage',
        ),
        migrations.RemoveField(
            model_name='aircraft',
            name='tail',
        ),
        migrations.RemoveField(
            model_name='aircraft',
            name='wing',
        ),
        migrations.AddField(
            model_name='part',
            name='assembled_aircraft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='rental.aircraft'),
        ),
    ]
