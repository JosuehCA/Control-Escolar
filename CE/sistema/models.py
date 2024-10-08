from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class Menu(models.Model):
    pass

class Salon(models.Model):
    """TDA Salón. Define aquellos grupos a los que pertenece un conjunto de estudiantes bajo la dirección 
    de un profesor."""

    nombre = models.CharField(max_length=2000)

    def __str__(self):
        return f'Salon: {self.nombre}'
    
    class Meta:
        verbose_name = "Salón"
        verbose_name_plural = "Salones"

# Reportes -------------------------------------------------------------------------------------

class Reporte(models.Model):
    """TDA Reporte. Define una entidad reporte cuyos valores dependen del tipo de reporte
    requerido (Reporte Individual, Reporte por Salón o Reporte General)."""

    fecha = models.DateTimeField(auto_now_add=True)


class ServicioReportes(models.Model):
    reporteActual = models.ForeignKey(Reporte, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True


class ReporteAlumno(ServicioReportes):
    class Meta:
        verbose_name = "Reporte Alumno"
        verbose_name_plural = "Reportes: Alumnos"


class ReporteSalon(ServicioReportes):
    class Meta:
        verbose_name = "Reporte Salon"
        verbose_name_plural = "Reportes: Salones"


class ReporteGlobal(ServicioReportes):
    class Meta:
        verbose_name = "Reporte Global"
        verbose_name_plural = "Reportes: Globales"


# Roles ---------------------------------------------------------------------------------------

class Usuario(AbstractUser):
    pass


class Administrador(Usuario):
    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"


class Profesor(Usuario):
    salon = models.ForeignKey(Salon, on_delete=models.RESTRICT, related_name="salon_profesor")

    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"


class Tutor(Usuario):
    class Meta:
        verbose_name = "Tutor"
        verbose_name_plural = "Tutores"


class Alumno(Usuario):
    tutoralumno = models.ForeignKey(Tutor, on_delete=models.RESTRICT, related_name="tutor_alumno")

    class Meta:
        verbose_name = "Alumno"
        verbose_name_plural = "Alumnos"


class Nutricionista(Usuario):
    class Meta:
        verbose_name = "Nutricionista"
        verbose_name_plural = "Nutricionistas"


# Mensajes -------------------------------------------------------------------------------------

class Mensaje(models.Model):
    emisor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contenido = models.CharField(max_length=2000)
    fechaEnviado = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class MensajeDirecto(Mensaje):
    remitente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="remitente_mensaje")

    class Meta:
        verbose_name = "Mensaje Directo"
        verbose_name_plural = "Mensajes: Directos"


class MensajeSalon(Mensaje):
    remitente = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, related_name="remitente_mensaje_salon")

    class Meta:
        verbose_name = "Mensaje Salon"
        verbose_name_plural = "Mensajes: Salones"


class MensajeAnuncio(Mensaje):
    pass

    class Meta:
        verbose_name = "Mensaje Anuncio"
        verbose_name_plural = "Mensajes: Anuncios"


class Conversacion(models.Model):
    usuario1 = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, related_name="usuario1_convo")
    usuario1 = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, related_name="usuario2_convo")


    class Meta:
        verbose_name = "Conversacion"
        verbose_name_plural = "Conversaciones"


class Notificacion(models.Model):
    pass

    class Meta:
        verbose_name = "Notificacion"
        verbose_name_plural = "Notificaciones"