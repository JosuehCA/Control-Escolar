from typing import List
from django.db import models as m
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class MenuSemanal(m.Model):
    """TDA Menu. Define un Menú de comidas personalizable de acuerdo al administrador, y tomando en cuenta
    ciertas indicaciones que los tutores manifiesten."""

    nombre = m.CharField(max_length=100)
    fecha_inicio = m.DateField()
    fecha_fin = m.DateField()

    def __str__(self):
        return self.nombre

class Grupo(m.Model):
    """TDA Grupo. Define aquellos grupos a los que pertenece un conjunto de estudiantes bajo la dirección 
    de un profesor."""

    nombre = m.CharField(max_length=2000)
    

    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"


class Platillo(m.Model):
    DIAS_SEMANA = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
    ]
    
    nombre = m.CharField(max_length=200)
    descripcion = m.TextField()
    consideraciones = m.TextField(blank=True, null=True)
    dia = m.CharField(
        max_length=10,
        choices=DIAS_SEMANA,
        blank=True,  
        null=True,
        help_text="Día de la semana al que pertenece este platillo."
    )
    menu = m.ForeignKey(
        'MenuSemanal',
        on_delete=m.CASCADE,
        related_name='platillos',
        null=True,
        blank=True,
        help_text="Menú al que pertenece este platillo."
    )

    def __str__(self):
        return f"{self.nombre} ({self.dia or 'Sin Día'})"


class Actividad(m.Model):
    """TDA Actividad. Representa una actividad específica que los alumnos pueden realizar en un
    periodo de tiempo."""

    nombre = m.CharField(max_length=100)
    horaInicio = m.TimeField()
    horaFinal = m.TimeField()


    class Meta:
        verbose_name_plural = "Actividades"




# Roles ---------------------------------------------------------------------------------------


class UsuarioEscolar(AbstractUser):
    """TDA Usuario Escolar. Define el rol común entre todos aquellos pertenecientes a la institución de una
    u otra manera (profesores, admnistrador, tutores, alumnos y nutricionista). Proporciona actividades 
    comunes dentro de estos roles."""

    pass


    class Meta:
        verbose_name = "Usuario Escolar"
        verbose_name_plural = "Usuarios Escolares"



class Administrador(UsuarioEscolar):
    """TDA Administrador. Rol especial dentro del plantel cuyos permisos permiten controlar todo cuanto
    sea necesario. Tiene acceso a todos los apartados."""    

    @classmethod
    def crearGrupo(cls, nombre: str, alumnos: List['Alumno']) -> None:
        if not Grupo.objects.filter(nombre=nombre).exists():
            nuevo_grupo = Grupo(nombre=nombre)
            nuevo_grupo.save()  # Guardamos primero para poder asignar M2M
            nuevo_grupo.alumnos.set(alumnos)  # Añadimos los alumnos seleccionados al grupo
            nuevo_grupo.save()
        else:
            print("El grupo ya existe.")
            
    def alumnosNoTienenGrupo(alumnos: List['Alumno']) -> bool:
        for alumno in alumnos:
            if Grupo.objects.filter(alumnos=alumno).exists():
                return False  # El alumno ya pertenece a un grupo
        return True

    def eliminarGrupo(self, grupo_id: int) -> None:
        try:
            grupo = Grupo.objects.get(id=grupo_id)
            grupo.delete()
        except Grupo.DoesNotExist:
            print("El grupo no existe.")

    @classmethod
    def editarGrupo(cls, grupo_id: int, nombre: str, alumnos: List['Alumno']) -> None:
        try:
            grupo = Grupo.objects.get(id=grupo_id)
            grupo.nombre = nombre
            grupo.alumnos.set(alumnos)
            grupo.save()
        except Grupo.DoesNotExist:
            print("El grupo no existe.")
            
            
    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"



class Profesor(UsuarioEscolar):
    """TDA Profesor. Encargado de un subconjunto de grupos en específico y bajo mandato de un cierto grupo
    de alumnos. Contiene comportamientos respecto a estos alumnos, como asignación de actividades o pasar
    lista, y mantiene contacto directo con los tutores."""

    grupo = m.ForeignKey(Grupo, on_delete=m.RESTRICT, related_name="grupo_profesor")


    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"



class Tutor(UsuarioEscolar):
    """TDA Tutor. Tutor legal del alumno inscrito. Cuenta con acceso al sistema y puede visualizar toda la 
    información pertinente a sus tutorados."""

    pass


    class Meta:
        verbose_name = "Tutor"
        verbose_name_plural = "Tutores"



class Alumno(UsuarioEscolar):
    """TDA Alumno. Registrado solo para fines logísticos. Representa a cada alumno inscrito en el sistema y
    contiene un registro de su información académica."""

    tutoralumno = m.ForeignKey(Tutor, on_delete=m.RESTRICT, related_name="tutor_alumno")


    class Meta:
        verbose_name = "Alumno"
        verbose_name_plural = "Alumnos"



class Nutricionista(UsuarioEscolar):
    """TDA Nutricionista. Responsable de la administración correcta de las comidas y ajustes al menú."""

    def crearPlatillo(nombre: str, descripcion: str, consideraciones: str):
        Platillo.objects.create(
            nombre=nombre, 
            descripcion=descripcion, 
            consideraciones=consideraciones)
        
    

    class Meta:
        verbose_name = "Nutricionista"
        verbose_name_plural = "Nutricionistas"
