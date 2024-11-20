from django.http import HttpRequest, HttpResponse
#from weasyprint import HTML
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import base64
from django.template.loader import render_to_string
from io import BytesIO
from django.utils.timezone import localtime, now


from sistema.models.models import Alumno
from sistema.models.models_reportes import *

    
def crearDiagramaPastelCalificaciones() -> base64:
    # Crear gráfico de pastel Matplotlib
    figura, eje = plt.subplots()
    eje.pie([10, 20, 30, 40], labels=["Category A", "Category B", "Category C", "Category D"],
           autopct='%1.1f%%', startangle=90, colors=["#FF0000", "#00FF00", "#0000FF", "#FFFF00"])
    plt.axis('equal')  # Mantener relación de aspecto del gráfico

    # Guardar gráfico a objeto BytesIO y codificarlo como base 64
    imagenBinaria = BytesIO()
    plt.savefig(imagenBinaria, format='png')
    imagenBinaria.seek(0)
    plt.close()
    imagen = base64.b64encode(imagenBinaria.getvalue()).decode('utf-8')

    return imagen

def generarDiagramaPastel(request: HttpRequest) -> HttpResponse:

    diagramaBase64: base64 = crearDiagramaPastelCalificaciones()

    # Renderizar contenido HTML con texto base 64 del gráfico
    contenidoHTML = render_to_string("sistema/Vista_DiagramaPastel.html", {"imagenDiagramaPastelPNG": f"data:image/png;base64, {diagramaBase64}"})

    # Generar PDF con Weasyprint
    archivoPDFBinario = BytesIO()
    HTML(string=contenidoHTML).write_pdf(archivoPDFBinario)
    archivoPDFBinario.seek(0)

    return HttpResponse(archivoPDFBinario, content_type='application/pdf')

def crearReporteAsistencia(alumno: Alumno) -> base64:
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

    # Guardar gráfico como imagen base64
    imagenBinaria = BytesIO()
    plt.savefig(imagenBinaria, format='png')
    imagenBinaria.seek(0)
    plt.close()
    imagen = base64.b64encode(imagenBinaria.getvalue()).decode('utf-8')
    time = localtime(now())
    print(time)

    # Guardar reporte en la base de datos
    contenido = f"Asistencias: {asistencias}, Faltas: {faltas}, Porcentaje: {porcentaje_asistencia:.2f}%"
    ReporteAlumno.objects.create(alumno=alumno, contenido=contenido, fecha=time)

    return imagen

def generarReporteAsistencia(request: HttpRequest) -> HttpResponse:
    alumno = Alumno.objects.get(username="Alumno1")
    diagramaBase64 = crearReporteAsistencia(alumno)

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