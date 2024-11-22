from django.db import models as m
from .models import Grupo, Alumno, RegistroCalificaciones

import matplotlib.pyplot as plt
from django.utils.timezone import localtime, now

class Reporte(m.Model):
    """
    TDA Reporte. Define una entidad reporte cuyos valores dependen del tipo de reporte
    requerido (reporte grupal o reporte global).
    """

    fecha = m.DateTimeField(auto_now_add=True)
    contenido = m.TextField()


    class Meta:
        abstract = True


class ReporteGrupo(Reporte):
    """
    TDA Reporte de Grupo. Proporciona detalles condensados por grupos acerca de su calificación conductual o asistencias. 
    """
    
    grupo = m.ForeignKey(Grupo, on_delete=m.CASCADE)


    class Meta:
        verbose_name = "Reporte Grupo"
        verbose_name_plural = "Reportes: Grupos"

    def __str__(self):
        return f"Reporte de grupo '{self.grupo.nombre}', {self.fecha.strftime('%d-%m-%Y %I:%M:%S %p')}" 



class ReporteGlobal(Reporte):
    """
    TDA Reporte Global. Proporciona detalles de calificaciones conductuales o de asistencia de todos los alumnos inscritos
    en el plantel.
    """

    class Meta:
        verbose_name = "Reporte Global"
        verbose_name_plural = "Reportes: Globales"

    def __str__(self):
        return f"Reporte global número {self.id}, {self.fecha.strftime('%d-%m-%Y %I:%M:%S %p')}"


class ManejadorReportes:
    """
    Clase para manejar la generación y almacenamiento de reportes en el sistema.
    """

    # Generar distintos tipos de reporte
    @staticmethod
    def generarHistogramaEnMemoria(tipo: str, alcance: str) -> None:
        """
        Genera un histograma de calificaciones en memoria, de acuerdo a una escala del 1 al 5.

        Argumentos:

            tipo_de_datos: (faltas/calificaciones). Tipo de datos sobre los cuales queremos trabajar.

            alcance: (global/grupo:nombre_de_grupo). Área sobre la cual queremos obtener los datos.
        """
        grupo_nombre = None

        # Obtenemos el tipo de alcance para delimitar la población de alumnos
        if alcance.startswith("grupo:"):
            grupo_nombre = alcance.removeprefix("grupo:").strip()
            alumnos = Alumno.objects.filter(grupo__nombre=grupo_nombre)
        elif alcance == "global":
            alumnos = Alumno.objects.all()
        else:
            raise ValueError("Alcance inválido. Debe ser 'grupo:nombre_grupo' o 'global'.")

        figura, eje = plt.subplots()

        if tipo == "calificaciones":
            # Obtener calificaciones de los alumnos
            calificaciones = (
                RegistroCalificaciones.objects.filter(alumno__in=alumnos)
                .values_list("calificacion", flat=True)
            )

            # Construir histograma con MatPlot
            eje.hist(calificaciones, bins=range(1, 7), color="#00FF00", edgecolor="black", align="left", rwidth=0.8)
            eje.set_title(f"Histograma de Calificaciones ({f'Grupo: {grupo_nombre}' if grupo_nombre else 'Global'})")
            eje.set_xlabel("Calificaciones (1-5)")
            eje.set_xticks(range(1, 6))
        else:
            raise ValueError("Tipo inválido. Debe ser 'faltas' o 'calificaciones'.")
        
        eje.set_ylabel("Número de Alumnos")
        plt.tight_layout()


    @staticmethod
    def generarDiagramaPastelEnMemoria(tipo_de_datos: str, alcance: str, colores: list) -> None:
        """
        Genera un diagrama de pastel de faltas en memoria, de acuerdo a <1, 2, 3 o >4 faltas.

        Argumentos:

            tipo_de_datos: (faltas/calificaciones). Tipo de datos sobre los cuales queremos trabajar.

            alcance: (global/grupo:nombre_de_grupo). Área sobre la cual queremos obtener los datos.

            colores: Lista de colores con los cuales deseamos trabajar.
        """

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

        # Construir diagrama con MatPlot
        figura, eje = plt.subplots()
        eje.pie(valores_filtrados, labels=etiquetas_filtradas, autopct='%1.1f%%', startangle=90, 
                colors=colores_filtrados)
        plt.axis('equal')

        resultadoTextual = {etiqueta: f"{porcentaje:.1f}%" for etiqueta, porcentaje in zip(etiquetas_filtradas, porcentajes)}

        if alcance.startswith("grupo:"):
            ManejadorReportes._guardarReporteGrupo(alcance.removeprefix("grupo:"), resultadoTextual)
        elif alcance == "global":
            ManejadorReportes._guardarReporteGlobal(resultadoTextual)


# Métodos privados -------------------------------------------------------------------

    @staticmethod
    def _obtenerDispersionFaltasAlumnado(alcance: str) -> tuple[int]:
        """
        Devuelve estadísticas de faltas del alumnado de acuerdo a la población definida.

        Argumentos:

            alcance: (global/grupo:nombre_de_grupo). Área sobre la cual queremos obtener los datos.
        """
        faltas_1_o_menos = 0
        faltas_2 = 0
        faltas_3 = 0
        faltas_4_o_mas = 0

        conjuntoDeAlumnos = conjuntoDeAlumnos = Alumno.objects.all()

        if alcance.startswith("grupo:"):
            conjuntoDeAlumnos = Alumno.objects.filter(grupo__nombre=alcance.split(":")[1].strip())

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
        """
        Guarda un reporte generado de un grupo específico.

        Argumentos:

            grupo: Nombre del grupo solicitado.

            contenido: Contenido en texto plano del reporte.
        """
        try:
            grupo: Grupo = Grupo.objects.get(nombre=grupo)

            ReporteGrupo.objects.create(grupo=grupo, contenido=contenido, fecha=now())
        except Grupo.DoesNotExist:
            raise ValueError("Grupo no encontrado")

    @staticmethod
    def _guardarReporteGlobal(contenido: str) -> None:
        """
        Guarda un reporte generado de todo el alumnado.

        Argumentos:

            contenido: Contenido en texto plano del reporte.
        """
        ReporteGlobal.objects.create(contenido=contenido, fecha=now())
