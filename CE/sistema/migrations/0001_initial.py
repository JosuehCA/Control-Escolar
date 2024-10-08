# Generated by Django 4.1.2 on 2024-10-08 17:53

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsuarioEscolar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('horaInicio', models.TimeField()),
                ('horaFinal', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=2000)),
            ],
            options={
                'verbose_name': 'Grupo',
                'verbose_name_plural': 'Grupos',
            },
        ),
        migrations.CreateModel(
            name='Mensajero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Notificacion',
                'verbose_name_plural': 'Notificaciones',
            },
        ),
        migrations.CreateModel(
            name='Plato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('usuarioescolar_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Administrador',
                'verbose_name_plural': 'Administradores',
            },
            bases=('sistema.usuarioescolar',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Nutricionista',
            fields=[
                ('usuarioescolar_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Nutricionista',
                'verbose_name_plural': 'Nutricionistas',
            },
            bases=('sistema.usuarioescolar',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('usuarioescolar_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Tutor',
                'verbose_name_plural': 'Tutores',
            },
            bases=('sistema.usuarioescolar',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ReporteGrupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reporteActual', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sistema.reporte')),
            ],
            options={
                'verbose_name': 'Reporte Grupo',
                'verbose_name_plural': 'Reportes: Grupos',
            },
        ),
        migrations.CreateModel(
            name='ReporteGlobal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reporteActual', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sistema.reporte')),
            ],
            options={
                'verbose_name': 'Reporte Global',
                'verbose_name_plural': 'Reportes: Globales',
            },
        ),
        migrations.CreateModel(
            name='ReporteAlumno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reporteActual', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sistema.reporte')),
            ],
            options={
                'verbose_name': 'Reporte Alumno',
                'verbose_name_plural': 'Reportes: Alumnos',
            },
        ),
        migrations.CreateModel(
            name='MensajeGrupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.CharField(max_length=2000)),
                ('fechaEnviado', models.DateTimeField(auto_now_add=True)),
                ('emisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('remitente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='remitente_mensaje_grupo', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Mensaje Grupo',
                'verbose_name_plural': 'Mensajes: Grupos',
            },
        ),
        migrations.CreateModel(
            name='MensajeDirecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.CharField(max_length=2000)),
                ('fechaEnviado', models.DateTimeField(auto_now_add=True)),
                ('emisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Mensaje Directo',
                'verbose_name_plural': 'Mensajes: Directos',
            },
        ),
        migrations.CreateModel(
            name='MensajeAnuncio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.CharField(max_length=2000)),
                ('fechaEnviado', models.DateTimeField(auto_now_add=True)),
                ('emisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Mensaje Anuncio',
                'verbose_name_plural': 'Mensajes: Anuncios',
            },
        ),
        migrations.CreateModel(
            name='Conversacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario1', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='usuario1_convo', to=settings.AUTH_USER_MODEL)),
                ('usuario2', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='usuario2_convo', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Conversacion',
                'verbose_name_plural': 'Conversaciones',
            },
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('usuarioescolar_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='grupo_profesor', to='sistema.grupo')),
            ],
            options={
                'verbose_name': 'Profesor',
                'verbose_name_plural': 'Profesores',
            },
            bases=('sistema.usuarioescolar',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('usuarioescolar_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('tutoralumno', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='tutor_alumno', to='sistema.tutor')),
            ],
            options={
                'verbose_name': 'Alumno',
                'verbose_name_plural': 'Alumnos',
            },
            bases=('sistema.usuarioescolar',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
