from typing import List
|from django.db import models as m
from django.conf import settings

class Menu(m.Model):
    """TDA Menu. Define un Menú de comidas personalizable de acuerdo al administrador, y tomando en cuenta
    ciertas indicaciones que los tutores manifiesten."""

    pass


class Grupo(m.Model):
    """TDA Salón. Define aquellos grupos a los que pertenece un conjunto de estudiantes bajo la dirección 
    de un profesor."""

    nombre = m.CharField(max_length=2000)
    alumnos = m.ManyToManyField('Alumno', related_name="alumnosGrupo")

    def __str__(self):
        return f'Grupo: {self.nombre}'
    
    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"


class Plato(m.Model):
    """TDA Plato. Modela un platillo disponible en el menú, incluyendo el nombre, descripción del mismo y 
    consideraciones."""

    nombre = m.CharField(max_length=200)
    descripcion = m.CharField(max_length=300)
    #consideraciones


class Actividad(m.Model):
    """TDA Actividad. Representa una actividad específica que los alumnos pueden realizar en un
    periodo de tiempo."""

    nombre = m.CharField(max_length=100)
    horaInicio = m.TimeField()
    horaFinal = m.TimeField()

    class Meta:
        verbose_name_plural = "Actividades"


# Reportes -------------------------------------------------------------------------------------

class Reporte(m.Model):
    """TDA Reporte. Define una entidad reporte cuyos valores dependen del tipo de reporte
    requerido (Reporte Individual, Reporte por Salón o Reporte Global)."""

    fecha = m.DateTimeField(auto_now_add=True)


class ServicioReportes(m.Model):
    """Tda Servicio de Reportes. Proporciona una interfaz para obtener reportes de diversos tipos,
    teniendo como base un departamento específico."""

    reporteActual = m.ForeignKey(Reporte, on_delete=m.SET_NULL, null=True)

    class Meta:
        abstract = True


class ReporteAlumno(ServicioReportes):
    """TDA Reporte de Alumno. Reporte individual por alumno que registra detalles conductuales, de asistencias,
    entre otros."""

    class Meta:
        verbose_name = "Reporte Alumno"
        verbose_name_plural = "Reportes: Alumnos"


class ReporteGrupo(ServicioReportes):
    """TDA Reporte de Grupo. Proporciona detalles condensados por grupos de conducta, asistencias, entre 
    otros."""

    class Meta:
        verbose_name = "Reporte Grupo"
        verbose_name_plural = "Reportes: Grupos"


class ReporteGlobal(ServicioReportes):
    """TDA Reporte Global. Proporciona detalles conductuales y de asistencia de todos los alumnos inscritos
    en el plantel."""

    class Meta:
        verbose_name = "Reporte Global"
        verbose_name_plural = "Reportes: Globales"


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


    def crearGrupo(self, nombre: str, alumnos: List['Alumno']) -> None:
        if not Grupo.objects.filter(nombre=nombre).exists():
            nuevo_grupo = Grupo(nombre=nombre)
            nuevo_grupo.save()  # Guardamos primero para poder asignar M2M
            nuevo_grupo.alumnos.set(alumnos)  # Añadimos los alumnos seleccionados al grupo
            nuevo_grupo.save()
        else:
            print("El grupo ya existe.")


    def eliminarGrupo(self, grupo_id: int) -> None:
        try:
            grupo = Grupo.objects.get(id=grupo_id)
            grupo.delete()
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

    class Meta:
        verbose_name = "Nutricionista"
        verbose_name_plural = "Nutricionistas"


# Mensajes -------------------------------------------------------------------------------------

class Mensaje(m.Model):
    """TDA Mensaje. Define la estructura de un mensaje dentro del mensajero virtual."""

    emisor = m.ForeignKey(UsuarioEscolar, on_delete=m.CASCADE)
    contenido = m.CharField(max_length=2000)
    fechaEnviado = m.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class MensajeDirecto(Mensaje):
    """TDA Mensaje Directo. Particulariza un mensaje de manera individual."""# Maybe añadir vistos?

    class Meta:
        verbose_name = "Mensaje Directo"
        verbose_name_plural = "Mensajes: Directos"


class MensajeGrupo(Mensaje):
    """TDA Mensaje de Grupo. Particulariza un mensaje de manera grupal."""

    remitente = m.ForeignKey(UsuarioEscolar, on_delete=m.DO_NOTHING, related_name="remitente_mensaje_grupo")

    class Meta:
        verbose_name = "Mensaje Grupo"
        verbose_name_plural = "Mensajes: Grupos"


class MensajeAnuncio(Mensaje):
    """TDA Mensaje Anuncio. Establece un mensaje compartido de manera global a todo el plantel."""

    pass

    class Meta:
        verbose_name = "Mensaje Anuncio"
        verbose_name_plural = "Mensajes: Anuncios"


class Mensajero(m.Model):
    """TDA Mensajero. Modela el mensajero virtual presente en el sistema y propio de cada usuario 
    registrado."""

    pass


class Conversacion(m.Model):
    """TDA Conversacion. Representa una conversacion individual entre dos partes registradas en el sistema."""

    usuario1 = m.ForeignKey(UsuarioEscolar, on_delete=m.DO_NOTHING, related_name="usuario1_convo")
    usuario2 = m.ForeignKey(UsuarioEscolar, on_delete=m.DO_NOTHING, related_name="usuario2_convo")


    class Meta:
        verbose_name = "Conversacion"
        verbose_name_plural = "Conversaciones"


class Notificacion(m.Model):
    """TDA Notificacion. Representa una notificación en particular."""

    pass

    class Meta:
        verbose_name = "Notificacion"
