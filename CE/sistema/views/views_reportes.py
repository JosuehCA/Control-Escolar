from django.http import HttpRequest, HttpResponse
from weasyprint import HTML
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from django.template.loader import render_to_string
from io import BytesIO
from django.utils.timezone import localtime, now
from django.shortcuts import render, redirect
from sistema.models.forms_lista import *


from sistema.models.models import Alumno
from sistema.models.models_reportes import *


def obtenerDiagramaPastel(request: HttpRequest, tipo: str) -> HttpResponse:

    if tipo.lower() == "faltas":
        faltas = ManejadorReportes.obtenerDispersionFaltasAlumnado()
        diagramaBase64 = ManejadorReportes.generarDiagramaPastelFaltas(faltas)

    elif tipo.lower() == "calificaciones":
        valores = [10, 20, 30, 40]
        etiquetas = ["Excelente", "Bueno", "Regular", "Deficiente"]
        diagramaBase64 = ManejadorReportes.generarDiagramaPastelCalificaciones(valores, etiquetas)


    contenidoHTML = render_to_string("sistema/Vista_DiagramaPastel.html", {
        "imagenDiagramaPastelPNG": f"data:image/png;base64, {diagramaBase64}",
        "titulo": tipo
    })

    archivoPDFBinario = BytesIO()
    HTML(string=contenidoHTML).write_pdf(archivoPDFBinario)
    archivoPDFBinario.seek(0)

    return HttpResponse(archivoPDFBinario, content_type='application/pdf')

def generarReporteAsistenciaIndividual(alumno: Alumno) -> int:
    # Datos de asistencia
    asistencias = alumno.getAsistencias()
    faltas = alumno.getFaltas()
    total_clases = asistencias + faltas
    porcentaje_asistencia = (asistencias / total_clases) * 100 if total_clases > 0 else 0

    # Crear gráfico de barras
    figura, eje = plt.subplots()
    barras = eje.bar(["Asistencias", "Faltas"], [asistencias, faltas], color=["#00FF00", "#FF0000"])
    for barra in barras:
        eje.text(barra.get_x() + barra.get_width() / 2, barra.get_height() / 2, f'{int(barra.get_height())}', ha='center')

    eje.set_title(f"Reporte de Asistencia de {alumno.getNombre()}")
    eje.set_ylabel('Clases')

    return porcentaje_asistencia

def crearImagenReporteAsistenciaIndividual(alumno: Alumno) -> base64:
    
    razonDeFaltas = generarReporteAsistenciaIndividual(alumno)

    # Guardar gráfico como imagen base64
    imagenBinaria = BytesIO()
    plt.savefig(imagenBinaria, format='png')
    imagenBinaria.seek(0)
    plt.close()
    imagen = base64.b64encode(imagenBinaria.getvalue()).decode('utf-8')
    time = localtime(now())
    print(time)

    # Guardar reporte en la base de datos
    contenido = f"Asistencias: {alumno.getAsistencias()}, Faltas: {alumno.getFaltas()}, Porcentaje: {razonDeFaltas:.2f}%"
    ReporteAlumno.objects.create(alumno=alumno, contenido=contenido, fecha=time)

    return imagen

def obtenerHistogramaAsistencias(request: HttpRequest) -> HttpResponse:
    alumno_id = request.GET.get('alumno_id')

    if not alumno_id:
        return render(request, "sistema/Vista_Error.html", {
            "mensaje_error": "No se proporcionó un ID de alumno. Por favor, seleccione un alumno válido."
        })

    try:
        alumno = Alumno.objects.get(id=alumno_id)
    except Alumno.DoesNotExist:
        return render(request, "sistema/Vista_Error.html", {
            "mensaje_error": f"No se encontró un alumno con el ID {alumno_id}. Por favor, seleccione un alumno válido."
        })

    diagramaBase64 = crearImagenReporteAsistenciaIndividual(alumno)

    cantidadAsistencias: int = alumno.getAsistencias()
    cantidadFaltas: int = alumno.getFaltas()

    if cantidadAsistencias + cantidadFaltas > 0:
        porcentajeAsistencia = (cantidadAsistencias / (cantidadAsistencias + cantidadFaltas) * 100)
    else:
        porcentajeAsistencia = 0

    contenidoHTML = render_to_string("sistema/Vista_ReporteAsistencia.html", {
        "imagenAsistenciaPNG": f"data:image/png;base64, {diagramaBase64}",
        "nombre_alumno": f"{alumno.getNombre()}",
        "asistencias": cantidadAsistencias,
        "faltas": cantidadFaltas,
        "porcentaje_asistencia": f"{porcentajeAsistencia:.2f}"
    })

    archivoPDFBinario = BytesIO()
    HTML(string=contenidoHTML).write_pdf(archivoPDFBinario)
    archivoPDFBinario.seek(0)

    return HttpResponse(archivoPDFBinario, content_type='application/pdf')

def actualizarAsistencias(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AsistenciaForm(request.POST)
        if form.is_valid():
            alumno: Alumno = form.cleaned_data['alumno']
            asistencias = form.cleaned_data['asistencias']
            faltas = form.cleaned_data['faltas']

            alumno.setAsistencias(asistencias)
            alumno.setFaltas(faltas)
            alumno.save()

            return redirect('reportes_disponibles')  # Redirigir a la página de reportes

    else:
        form = AsistenciaForm()

    return render(request, "sistema/Vista_ActualizarAsistencias.html", {"form": form})

def reportesDisponibles(request: HttpRequest) -> HttpResponse:
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

    diagramaBase64 = ManejadorReportes.generarHistogramaAsistenciaIndividual(alumno)
    porcentajeAsistencia = alumno.getAsistencias() / (alumno.getAsistencias() + alumno.getFaltas()) * 100 if (alumno.getAsistencias() + alumno.getFaltas()) > 0 else 0
    contenido = f"Asistencias: {alumno.getAsistencias()}, Faltas: {alumno.getFaltas()}, Porcentaje: {porcentajeAsistencia:.2f}%"
    
    ManejadorReportes.guardarReporteAlumno(alumno, contenido)

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