from django.db import models as m
from django.conf import settings
from .models import Grupo, Alumno

import matplotlib.pyplot as plt
import base64
from io import BytesIO
from django.utils.timezone import localtime, now

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


class ManejadorReportes:
    """Clase para manejar la generación y almacenamiento de reportes en el sistema."""


    # Generar distintos tipos de reporte
    @staticmethod
    def generarHistogramaCalificacionesBase64(alumno: Alumno) -> str:
        # Crear gráfico de barras
        figura, eje = plt.subplots()
        barras = eje.bar(["Asistencias", "Faltas"], [alumno.getAsistencias(), alumno.getFaltas()], color=["#00FF00", "#FF0000"])
        for barra in barras:
            eje.text(barra.get_x() + barra.get_width() / 2, barra.get_height() / 2, f'{int(barra.get_height())}', ha='center')

        eje.set_title(f"Reporte de Asistencia de {alumno.getNombre()}")
        eje.set_ylabel('Clases')

        return ManejadorReportes._codificarImagenBase64DesdeMemoria()

    @staticmethod
    def generarDiagramaPastelBase64(tipo: str, etiquetas: list, colores: list) -> str:
        """Genera un diagrama de pastel de faltas y lo devuelve como imagen base64."""

        if tipo == "falas":
            valores = ManejadorReportes._obtenerDispersionFaltasAlumnado()

        # Filtrar etiquetas y colores para faltas mayores a 0
        valores_filtrados = [v for v in valores if v > 0]
        etiquetas_filtradas = [etiquetas[i] for i, v in enumerate(valores) if v > 0]
        colores_filtrados = [colores[i] for i, v in enumerate(valores) if v > 0]

        # Crear la figura y el gráfico
        figura, eje = plt.subplots()
        eje.pie(valores_filtrados, labels=etiquetas_filtradas, autopct='%1.1f%%', startangle=90, 
                colors=colores_filtrados)
        plt.axis('equal')  # Mantener relación de aspecto del gráfico

        return ManejadorReportes._codificarImagenBase64DesdeMemoria()

    # Guardar tipos de reportes en la base de datos
    @staticmethod
    def guardarReporteAlumno(alumno: Alumno, contenido: str) -> None:
        """Guarda un reporte individual para un alumno."""
        ReporteAlumno.objects.create(alumno=alumno, contenido=contenido, fecha=now())

    @staticmethod
    def guardarReporteGrupo(grupo: Grupo, contenido: str) -> None:
        """Guarda un reporte para un grupo."""
        ReporteGrupo.objects.create(grupo=grupo, contenido=contenido, fecha=now())

    @staticmethod
    def guardarReporteGlobal(contenido: str) -> None:
        """Guarda un reporte global."""
        ReporteGlobal.objects.create(contenido=contenido, fecha=now())


    # Métodos privados
    @staticmethod
    def _codificarImagenBase64DesdeMemoria() -> str:
        """Codifica en base64 la imagen actual de Matplotlib."""
        imagenBinaria = BytesIO()
        plt.savefig(imagenBinaria, format='png')
        imagenBinaria.seek(0)
        plt.close()
        return base64.b64encode(imagenBinaria.getvalue()).decode('utf-8')
    
    @staticmethod
    def _obtenerDispersionFaltasAlumnado() -> tuple[int]:
        """Devuelve estadísticas de faltas del alumnado."""
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
