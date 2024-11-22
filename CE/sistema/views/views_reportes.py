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


def obtenerDiagramaPastel(request: HttpRequest, tipo: str) -> HttpResponse:

    colores = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00"]

    if tipo.lower() == "faltas":
        etiquetas = ["1 falta o menos", "2 faltas", "3 faltas", "4 o más faltas"]

        diagramaBase64 = ManejadorReportes.generarDiagramaPastelBase64(tipo.lower(), etiquetas, colores)


    contenidoHTML = render_to_string("sistema/Vista_DiagramaPastel.html", {
        "imagenDiagramaPastelPNG": f"data:image/png;base64, {diagramaBase64}",
        "titulo": tipo
    })

    archivoPDFBinario = BytesIO()
    HTML(string=contenidoHTML).write_pdf(archivoPDFBinario)
    archivoPDFBinario.seek(0)

    return HttpResponse(archivoPDFBinario, content_type='application/pdf')

def actualizarAsistencias(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AsistenciaForm(request.POST)
        if form.is_valid():
            
            _obtenerYGuardarAsistenciasYFaltasEnBD(form)

            return redirect('reportes_disponibles')  # Redirigir a la página de reportes

    else:
        form = AsistenciaForm()

    return render(request, "sistema/Vista_ActualizarAsistencias.html", {"form": form})

def _obtenerYGuardarAsistenciasYFaltasEnBD(form: AsistenciaForm) -> None:
    alumno: Alumno = form.cleaned_data['alumno']
    asistencias = form.cleaned_data['asistencias']
    faltas = form.cleaned_data['faltas']

    alumno.setAsistencias(asistencias)
    alumno.setFaltas(faltas)
    alumno.save()

def obtenerReportesDisponibles(request: HttpRequest) -> HttpResponse:
    alumnos = Alumno.objects.all()
    return render(request, "sistema/Vista_ReportesDisponibles.html", {"alumnos": alumnos})

def obtenerHistogramaAsistencias(request: HttpRequest) -> HttpResponse:
    

    alumno_id = request.GET.get('alumno_id')
    if not alumno_id:
        return render(request, "sistema/Vista_Error.html", {
            "mensaje_error": "No se proporcionó un ID de alumno."
        })

    try:
        alumno = Alumno.objects.get(id=alumno_id)
    except Alumno.DoesNotExist:
        return render(request, "sistema/Vista_Error.html", {
            "mensaje_error": f"No se encontró un alumno con ID {alumno_id}."
        })

    diagramaBase64 = ManejadorReportes.generarHistogramaCalificacionesBase64(alumno)
    porcentajeAsistencia = alumno.getAsistencias() / (alumno.getAsistencias() + alumno.getFaltas()) * 100 if (alumno.getAsistencias() + alumno.getFaltas()) > 0 else 0
    contenido = f"Asistencias: {alumno.getAsistencias()}, Faltas: {alumno.getFaltas()}, Porcentaje: {porcentajeAsistencia:.2f}%"
    
    contenidoHTML = render_to_string("sistema/Vista_ReporteAsistencia.html", {
        "imagenAsistenciaPNG": f"data:image/png;base64, {diagramaBase64}",
        "nombre_alumno": alumno.getNombre(),
        "asistencias": alumno.getAsistencias(),
        "faltas": alumno.getFaltas(),
        "porcentaje_asistencia": f"{porcentajeAsistencia:.2f}"
    })

    archivoPDFBinario = BytesIO()
    HTML(string=contenidoHTML).write_pdf(archivoPDFBinario)
    archivoPDFBinario.seek(0)

    return HttpResponse(archivoPDFBinario, content_type='application/pdf')
