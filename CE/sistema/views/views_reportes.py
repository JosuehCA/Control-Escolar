from django.http import HttpRequest, HttpResponse
from weasyprint import HTML
import matplotlib
matplotlib.use('Agg')
from django.template.loader import render_to_string
from io import BytesIO
from django.shortcuts import render, redirect
import base64


from sistema.models.models import Alumno
from sistema.models.models_reportes import *

def obtenerHistogramaPDF(request: HttpRequest, tipo_de_datos: str, alcance: str) -> HttpResponse:
    """
    Proveniente de una solicitud, devuelve una respuesta HTTP de un documento PDF con el tipo de histograma solicitado.

    Argumentos:

        tipo_de_datos: (faltas/calificaciones). Tipo de datos sobre los cuales queremos trabajar.

        alcance: (global/grupo:nombre_de_grupo). Área sobre la cual queremos obtener los datos.
    """

    ManejadorReportes.generarHistogramaEnMemoria(tipo_de_datos, alcance)
    diagramaBase64 = _codificarImagenBase64DesdeMemoria()

    titulo: str = alcance

    if alcance.startswith("grupo:"):
        titulo = alcance.removeprefix("grupo:").strip()
    
    
    contenidoHTML = render_to_string("sistema/Vista_ReporteAsistencia.html", {
        "imagenAsistenciaPNG": f"data:image/png;base64, {diagramaBase64}",
        "titulo": titulo
    })

    return _generarPDF(contenidoHTML)

def obtenerDiagramaPastelPDF(request: HttpRequest, tipo_de_datos: str, alcance: str) -> HttpResponse:
    """
    Proveniente de una solicitud, devuelve respuesta HTTP de un documento PDF con el tipo de diagrama de pastel solicitado.

    Argumentos:
    
        tipo_de_datos: (faltas/calificaciones). Tipo de datos sobre los cuales queremos trabajar.

        alcance: (global/grupo:nombre_de_grupo). Área sobre la cual queremos obtener los datos.
    """

    colores = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00"]

    ManejadorReportes.generarDiagramaPastelEnMemoria(tipo_de_datos.lower(), alcance.lower(), colores)
    diagramaBase64 = _codificarImagenBase64DesdeMemoria()


    contenidoHTML = render_to_string("sistema/Vista_DiagramaPastel.html", {
        "imagenDiagramaPastelPNG": f"data:image/png;base64, {diagramaBase64}",
        "titulo": tipo_de_datos
    })

    return _generarPDF(contenidoHTML)


def obtenerReportesDisponibles(request: HttpRequest) -> HttpResponse:
    """
    Proveniente de una solicitud, devuelve una respuesta HTTP con los tipos de reportes disponibles.
    """

    alumnos = Alumno.objects.all()
    return render(request, "sistema/Vista_ReportesDisponibles.html", {"alumnos": alumnos})


# Métodos privados ----------------------------------------------------------------------

def _codificarImagenBase64DesdeMemoria() -> str:
    """
    Codifica en base64 la imagen actual guardada en memoria y la devuelve.
    """

    imagenBinaria = BytesIO()
    plt.savefig(imagenBinaria, format='png')
    imagenBinaria.seek(0)
    plt.close()
    return base64.b64encode(imagenBinaria.getvalue()).decode('utf-8')

def _generarPDF(contenidoHTML: str) -> HttpResponse:
    """
    Renderiza contenido HTML para devolverlo a manera de documento PDF.

    Argumentos:

        contenidoHTML: Texto en HTML sobre el cual queremos renderizar como documento PDF.
    """

    archivoPDFBinario = BytesIO()
    HTML(string=contenidoHTML).write_pdf(archivoPDFBinario)
    archivoPDFBinario.seek(0)

    return HttpResponse(archivoPDFBinario, content_type='application/pdf')