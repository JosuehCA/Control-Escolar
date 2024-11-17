# Generated by Django 5.1.2 on 2024-11-17 03:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alumno',
            old_name='tutoralumno',
            new_name='tutorAlumno',
        ),
        migrations.AddField(
            model_name='alumno',
            name='actividadActual',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='actividadActual', to='sistema.actividad'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='asistencias',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='alumno',
            name='consideracionesMenu',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='alumno',
            name='faltas',
            field=models.IntegerField(default=0),
        ),
    ]
