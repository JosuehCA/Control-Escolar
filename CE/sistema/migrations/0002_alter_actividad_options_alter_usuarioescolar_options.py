# Generated by Django 4.1.2 on 2024-10-08 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actividad',
            options={'verbose_name_plural': 'Actividades'},
        ),
        migrations.AlterModelOptions(
            name='usuarioescolar',
            options={'verbose_name': 'Usuario Escolar', 'verbose_name_plural': 'Usuarios Escolares'},
        ),
    ]
