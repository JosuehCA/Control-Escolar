from django.shortcuts import render
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from .forms_msj import MensajeDirectoForm
from .models_msj import MensajeDirecto
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse



# Weasyprint
from weasyprint import HTML
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import base64
from django.template.loader import render_to_string
from io import BytesIO


from .models import UsuarioEscolar
from .models_reportes import *


def indice(request: HttpRequest):
    return render(request, "sistema/Vista_Indice.html")

def iniciarSesion(request: HttpRequest):
    if request.method == "POST":

        # Intentar iniciar sesión
        nombreUsuario = request.POST["nombre_usuario"]
        contrasena = request.POST["contrasena"]
        usuario = authenticate(request, username=nombreUsuario, password=contrasena)

        # Validar usuario existente
        if usuario is not None:
            login(request, usuario)
            return HttpResponseRedirect(reverse("indice"))
        else:
            return render(request, "sistema/Vista_IniciarSesion.html", {
                "mensaje": "Nombre de usuario o contraseña incorrectos."
            })
    else:
        return render(request, "sistema/Vista_IniciarSesion.html")
    
def cerrarSesion(request: HttpRequest):
    logout(request)
    return HttpResponseRedirect(reverse("indice"))

def registrarse(request: HttpRequest):
    if request.method == "POST":
        nombreUsuario = request.POST["nombre_usuario"]
        email = request.POST["email"]

        # Comparando contraseña confirmada
        contrasena = request.POST["contrasena"]   
        confirmacion = request.POST["confirmacion"]
        if contrasena != confirmacion:
            return render(request, "sistema/Vista_Registrarse.html", {
                "mensaje": "Las contraseñas no son iguales."
            })

        # Intentar crear usuario nuevo
        try:
            usuario = UsuarioEscolar.objects.create_user(nombreUsuario, email, contrasena)
            usuario.save()
        except IntegrityError:
            return render(request, "sistema/Vista_Registrarse.html", {
                "mensaje": "Nombre de usuario ocupado."
            })
        login(request, usuario)
        return HttpResponseRedirect(reverse("indice"))
    else:
        return render(request, "sistema/Vista_Registrarse.html")
    
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

    # Crear gráfico de barras para asistencia vs faltas
    figura, eje = plt.subplots()
    barras = eje.bar(["Asistencias", "Faltas"], [asistencias, faltas], color=["#00FF00", "#FF0000"])

    for barra in barras:
        altura = barra.get_height() 
        posicion_y = barra.get_y() + altura / 2 
        eje.text(barra.get_x() + barra.get_width() / 2, posicion_y, f'{int(altura)}', ha='center', va='center', color='black')

    # Configurar título y etiquetas
    eje.set_title(f"Reporte de Asistencia de {alumno.getNombre()}")
    eje.set_ylabel('Cantidad de Clases')

    # Opcional: Incluir porcentaje de asistencia en el gráfico
    eje.text(0.5, -max(asistencias, faltas) - 2, f'Asistencia: {porcentaje_asistencia:.2f}%', ha='center', color='black')

    # Guardar gráfico a objeto BytesIO y codificarlo como base 64
    imagenBinaria = BytesIO()
    plt.savefig(imagenBinaria, format='png')
    imagenBinaria.seek(0)
    plt.close()
    imagen = base64.b64encode(imagenBinaria.getvalue()).decode('utf-8')

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


def cocina(request: HttpRequest):
    pass

@login_required
def enviarMensajeDirecto(request: HttpRequest) -> HttpResponse:
    """Vista para enviar un mensaje directo."""

    if request.method == 'POST':
        mensajeDirectoForm = MensajeDirectoForm(request.POST)
        
        if mensajeDirectoForm.is_valid():
            mensajeDirectoInstancia = mensajeDirectoForm.save(commit=False)
            receptorUsuario = mensajeDirectoForm.cleaned_data.get('receptorUsuario')
            
            if mensajeDirectoInstancia.enviar(request.user, receptorUsuario):
                return redirect('mensaje_directo')
            else:
                mensajeDirectoForm.add_error(None, "No puedes enviarte mensajes a ti mismo.")
    
    else:
        mensajeDirectoForm = MensajeDirectoForm()

    mensajesUsuario = MensajeDirecto.obtenerMensajesFiltrados(request.user)

    return render(request, 'sistema/testMensajeria.html', {
        'form': mensajeDirectoForm,
        'mensajes': mensajesUsuario,
    })

def plantel(request: HttpRequest):
    pass