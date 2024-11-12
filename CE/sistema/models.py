from django.contrib.auth.models import AbstractUser
from django.db import models as m
from django.conf import settings


class Platillo(m.Model):
    """TDA Platillo. Modela un platillo disponible en el menú, incluyendo el nombre, descripción del mismo y 
    consideraciones."""

    nombre = m.CharField(max_length=200)
    descripcion = m.CharField(max_length=300)
    consideraciones = m.TextField(blank=True, null=True)


    def __str__(self):
        return self.nombre
    


class MenuPlatillo(m.Model):
    """Tabla Menu Platillo. Auxiliar en la relación muchos a muchos entre varios Platillos y Varios Menús
    Semanales. Incluye atributo de Fecha para su filtrado."""
    
    menu = m.ForeignKey("MenuSemanal", on_delete=m.CASCADE, related_name="opcionesMenu")
    platillo = m.ForeignKey(Platillo, on_delete=m.SET_NULL, null=True)
    fecha = m.DateField()


    class Meta: 
        unique_together = ('menu', 'platillo', 'fecha')


    def __str__(self):
        return f"{self.menu.nombre} - {self.platillo.nombre} el {self.fecha}"



class MenuSemanal(m.Model):
    """TDA Menu Semanal.. Define un Menú de comidas personalizable de acuerdo al nutricionista, y tomando en cuenta
    ciertas indicaciones que los tutores manifiesten."""

    nombre = m.CharField(max_length=100)
    opcionesDePlatillo = m.ManyToManyField(Platillo, through=MenuPlatillo, related_name="menús")
    

    def obtenerMenusDia(self):
        """Rutina que devuelve todas las opciones de Menús para cada día específico"""

        lista = {}
        for opcion in self.opcionesMenu.all():
            if opcion not in lista:
                lista[opcion.fecha] = []
            lista[opcion.fecha].append(opcion.platillo)
        
        return lista
    

    class Meta:
        verbose_name = "Menú Semanal"
        verbose_name_plural = "Menús Semanales"
    


class Grupo(m.Model):
    """TDA Grupo. Define aquellos grupos a los que pertenece un conjunto de estudiantes bajo la dirección 
    de un profesor."""

    nombre = m.CharField(max_length=2000)
    

    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"


    def __str__(self):
        return f'Grupo: {self.nombre}'



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

    pass


    class Meta:
        verbose_name = "Nutricionista"
        verbose_name_plural = "Nutricionistas"
