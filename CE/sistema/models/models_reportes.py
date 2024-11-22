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

    class Meta:
        verbose_name = "Reporte Global"
        verbose_name_plural = "Reportes: Globales"

    def __str__(self):
        return f"Reporte global número {self.id}, {self.fecha.strftime('%d-%m-%Y %I:%M:%S %p')}"


class ManejadorReportes:
    """Clase para manejar la generación y almacenamiento de reportes en el sistema."""

    # Generar distintos tipos de reporte
    @staticmethod
    def generarHistogramaEnMemoria(tipo: str, alcance: str) -> None:
        # Crear gráfico de barras
        figura, eje = plt.subplots()
        barras = eje.bar(["Asistencias", "Faltas"], [alumno.getAsistencias(), alumno.getFaltas()], color=["#00FF00", "#FF0000"])
        for barra in barras:
            eje.text(barra.get_x() + barra.get_width() / 2, barra.get_height() / 2, f'{int(barra.get_height())}', ha='center')

        eje.set_title(f"Reporte de Asistencia de {alumno.getNombre()}")
        eje.set_ylabel('Clases')

    @staticmethod
    def generarDiagramaPastelEnMemoria(tipo_de_datos: str, alcance: str, colores: list) -> None:
        """Genera un diagrama de pastel de faltas y lo devuelve como imagen base64."""

        etiquetas: list[str]

        if tipo_de_datos == "faltas":
            etiquetas = ["1 falta o menos", "2 faltas", "3 faltas", "4 o más faltas"]

            valores = ManejadorReportes._obtenerDispersionFaltasAlumnado(alcance)

        # Filtrar etiquetas y colores para faltas mayores a 0
        valores_filtrados = [v for v in valores if v > 0]
        etiquetas_filtradas = [etiquetas[i] for i, v in enumerate(valores) if v > 0]
        colores_filtrados = [colores[i] for i, v in enumerate(valores) if v > 0]

         # Calcular porcentajes
        total = sum(valores_filtrados)
        porcentajes = [(v / total) * 100 for v in valores_filtrados]

        
        figura, eje = plt.subplots()
        eje.pie(valores_filtrados, labels=etiquetas_filtradas, autopct='%1.1f%%', startangle=90, 
                colors=colores_filtrados)
        plt.axis('equal')

        resultadoTextual = {etiqueta: f"{porcentaje:.1f}%" for etiqueta, porcentaje in zip(etiquetas_filtradas, porcentajes)}

        if alcance[:5] == "grupo":
            ManejadorReportes._guardarReporteGrupo(alcance[6:], resultadoTextual)
        elif alcance == "global":
            ManejadorReportes._guardarReporteGlobal(resultadoTextual)


# Métodos privados -------------------------------------------------------------------

    @staticmethod
    def _obtenerDispersionFaltasAlumnado(alcance: str) -> tuple[int]:
        """Devuelve estadísticas de faltas del alumnado de acuerdo al alcance definido"""
        faltas_1_o_menos = 0
        faltas_2 = 0
        faltas_3 = 0
        faltas_4_o_mas = 0

        conjuntoDeAlumnos = conjuntoDeAlumnos = Alumno.objects.all()

        if alcance[:5] == "grupo":
            conjuntoDeAlumnos = [alumno for alumno in conjuntoDeAlumnos
                                if alumno.grupo and alumno.grupo.nombre == alcance[6:]]

        for alumno in conjuntoDeAlumnos:
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
    
    # Guardar tipos de reportes en la base de datos
    @staticmethod
    def _guardarReporteGrupo(grupo: str, contenido: str) -> None:
        """Guarda un reporte para un grupo."""

        try:
            grupo: Grupo = Grupo.objects.get(nombre=grupo)

            ReporteGrupo.objects.create(grupo=grupo, contenido=contenido, fecha=now())
        except:
            raise("Grupo no encontrado")

    @staticmethod
    def _guardarReporteGlobal(contenido: str) -> None:
        """Guarda un reporte global."""
        ReporteGlobal.objects.create(contenido=contenido, fecha=now())
