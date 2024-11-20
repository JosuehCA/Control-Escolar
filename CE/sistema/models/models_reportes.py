from django.db import models as m
from django.conf import settings
from .models import Grupo, Alumno

class Reporte(m.Model):
    """TDA Reporte. Define una entidad reporte cuyos valores dependen del tipo de reporte
    requerido (reporte por alumno, reporte por grupo o reporte global)."""

    fecha = m.DateTimeField(auto_now_add=True)
    contenido = m.TextField()


    class Meta:
        abstract = True



class ReporteAlumno(Reporte):
    """TDA Reporte de Alumno. Reporte individual por alumno que registra detalles conductuales, de asistencias,
    entre otros."""

    alumno: Alumno = m.ForeignKey("Alumno", on_delete=m.CASCADE, related_name="alumno_reporte")


    class Meta:
        verbose_name = "Reporte Alumno"
        verbose_name_plural = "Reportes: Alumnos"

    def __str__(self):
        return f"Reporte de {self.alumno.getNombre()}, {self.fecha.strftime('%d-%m-%Y %I:%M:%S %p')}"



class ReporteGrupo(Reporte):
    """TDA Reporte de Grupo. Proporciona detalles condensados por grupos acerca de su conducta, asistencias, 
    entre otros."""
    
    grupo = m.ForeignKey(Grupo, on_delete=m.CASCADE)


    class Meta:
        verbose_name = "Reporte Grupo"
        verbose_name_plural = "Reportes: Grupos"



class ReporteGlobal(Reporte):
    """TDA Reporte Global. Proporciona detalles conductuales y de asistencia de todos los alumnos inscritos
    en el plantel."""

    pass

    class Meta:
        verbose_name = "Reporte Global"
        verbose_name_plural = "Reportes: Globales"