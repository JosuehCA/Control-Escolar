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

    def __str__(self):
        return f"Reporte de {self.grupo.nombre}, {self.fecha.strftime('%d-%m-%Y %I:%M:%S %p')}"



class ReporteGlobal(Reporte):
    """TDA Reporte Global. Proporciona detalles conductuales y de asistencia de todos los alumnos inscritos
    en el plantel."""

    pass

    class Meta:
        verbose_name = "Reporte Global"
        verbose_name_plural = "Reportes: Globales"


class ManejadorReportes():
    """TDA Manejador de Reportes. Trabaja sobre los datos de los alumnos para proporcionar a los
    controladores correspondientes."""
    
    def obtenerFaltasAlumnado() -> tuple[int]:
        """Itera sobre todos los alumnos registrados y devuelve cuántos tienen 1 falta o menos, 2,
        3 o 4 o más"""

        faltas_1_o_menos = 0
        faltas_2 = 0
        faltas_3 = 0
        faltas_4_o_mas = 0

        alumnos = Alumno.objects.all()
        for alumno in alumnos:
            faltas = alumno.getFaltas()

            if faltas == 1 or faltas == 0:
                faltas_1_o_menos += 1
            elif faltas == 2:
                faltas_2 += 1
            elif faltas == 3:
                faltas_3 += 1
            elif faltas >= 4:
                faltas_4_o_mas += 1

        return (faltas_1_o_menos, faltas_2, faltas_3, faltas_4_o_mas)
    

    



    
