from django.http import HttpRequest, HttpResponse
from weasyprint import HTML
import matplotlib
matplotlib.use('Agg')
from django.template.loader import render_to_string
from io import BytesIO
from django.shortcuts import render, redirect
from sistema.models.forms_lista import *


from sistema.models.models import Alumno
from sistema.models.models_reportes import *

def obtenerHistograma(request: HttpRequest, tipo_de_datos: str, alcance: str) -> HttpResponse:
    

    ManejadorReportes.generarHistogramaEnMemoria(tipo_de_datos, alcance)
    diagramaBase64 = _codificarImagenBase64DesdeMemoria()

    titulo: str = alcance

    if alcance[:5] == "grupo":
        titulo = alcance[6:]
    
    
    contenidoHTML = render_to_string("sistema/Vista_ReporteAsistencia.html", {
        "imagenAsistenciaPNG": f"data:image/png;base64, {diagramaBase64}",
        "titulo": titulo
    })

    return _generarPDF(contenidoHTML)

def obtenerDiagramaPastel(request: HttpRequest, tipo_de_datos: str, alcance: str) -> HttpResponse:

    colores = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00"]

    ManejadorReportes.generarDiagramaPastelEnMemoria(tipo_de_datos.lower(), alcance.lower(), colores)
    diagramaBase64 = _codificarImagenBase64DesdeMemoria()


    contenidoHTML = render_to_string("sistema/Vista_DiagramaPastel.html", {
        "imagenDiagramaPastelPNG": f"data:image/png;base64, {diagramaBase64}",
        "titulo": tipo_de_datos
    })

    return _generarPDF(contenidoHTML)

def actualizarAsistencias(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AsistenciaForm(request.POST)
        if form.is_valid():
            
            _obtenerYGuardarAsistenciasYFaltasEnBD(form)

            return redirect('reportes_disponibles')  # Redirigir a la página de reportes

    else:
        form = AsistenciaForm()

    return render(request, "sistema/Vista_ActualizarAsistencias.html", {"form": form})


def obtenerReportesDisponibles(request: HttpRequest) -> HttpResponse:
    alumnos = Alumno.objects.all()
    return render(request, "sistema/Vista_ReportesDisponibles.html", {"alumnos": alumnos})


# Métodos privados ----------------------------------------------------------------------

def _obtenerYGuardarAsistenciasYFaltasEnBD(form: AsistenciaForm) -> None:
    alumno: Alumno = form.cleaned_data['alumno']
    asistencias = form.cleaned_data['asistencias']
    faltas = form.cleaned_data['faltas']

    alumno.setAsistencias(asistencias)
    alumno.setFaltas(faltas)
    alumno.save()

def _codificarImagenBase64DesdeMemoria() -> str:
        """Codifica en base64 la imagen actual de Matplotlib."""
        imagenBinaria = BytesIO()
        plt.savefig(imagenBinaria, format='png')
        imagenBinaria.seek(0)
        plt.close()
        return base64.b64encode(imagenBinaria.getvalue()).decode('utf-8')

def _generarPDF(contenidoHTML: str) -> HttpResponse:
    archivoPDFBinario = BytesIO()
    HTML(string=contenidoHTML).write_pdf(archivoPDFBinario)
    archivoPDFBinario.seek(0)

    return HttpResponse(archivoPDFBinario, content_type='application/pdf')