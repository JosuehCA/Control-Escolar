from django.shortcuts import render
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from .forms_msj import MensajeDirectoForm
from .models_mensajeria import MensajeDirecto
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse



# Weasyprint
#from weasyprint import HTML
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import base64
from django.template.loader import render_to_string
from io import BytesIO


from .models import UsuarioEscolar
from .models_reportes import *
from .models_mensajeria import *


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


def generarReporte(request: HttpRequest) -> HttpResponse:

    datos = {"nombre": "Sample Report", "contenido": "Test de creación de PDF's"}
    
    # Render the HTML template with data
    cadena_html = render(request, "sistema/Vista_Reporte.html", {"datos": datos}).content.decode()
    archivo_pdf = HTML(string=cadena_html).write_pdf()

    respuesta = HttpResponse(archivo_pdf, content_type="application/pdf")
    respuesta["Content-Disposition"] = "inline; filename=report.pdf"

    return respuesta

def cocina(request: HttpRequest):
    pass

def mostrarVistaConversacion(request: HttpRequest, servicioDeMensajeriaURL: str) -> HttpResponse:
    """Vista dinamica para conversaciones individuales, grupales o generales."""
    manejador = ManejadorVistaMensajeria()
    tipoDeConversacion = manejador.obtenerTipoDeConversacion(servicioDeMensajeriaURL)
    if request.method == 'POST':
        mensajeDirectoForm = MensajeDirectoForm(request.POST)
        mensajesUsuario = MensajeDirecto.obtenerMensajesFiltrados(request.user)
        
        if mensajeDirectoForm.is_valid():
            mensajeDirectoInstancia = mensajeDirectoForm.save(commit=False)
            receptorUsuario = mensajeDirectoForm.cleaned_data.get('receptorUsuario')
            
            if mensajeDirectoInstancia.enviar(request.user, receptorUsuario):
                return render(request, "sistema/Vista_Conversacion.html", {
                "titulo": "Conversación Privada",
                "mensajes": mensajesUsuario,
                "form": mensajeDirectoForm,})
            else:
                mensajeDirectoForm.add_error(None, "No puedes enviarte mensajes a ti mismo.")
    else:
        if(tipoDeConversacion == "privado"):
            mensajeDirectoForm = MensajeDirectoForm()
            mensajesUsuario = MensajeDirecto.obtenerMensajesFiltrados(request.user)

            return render(request, "sistema/Vista_Conversacion.html", {
                "titulo": "Conversación Privada",
                "mensajes": mensajesUsuario,
                "form": mensajeDirectoForm,
                "servicioDeMensajeriaURL": servicioDeMensajeriaURL,})
        
        elif(tipoDeConversacion == "grupo"):
            mensajesUsuario = MensajeDirecto.obtenerMensajesFiltrados(request.user)

            return render(request, "sistema/Vista_Conversacion.html", {
                "titulo": "Conversación Grupal",
                "mensajes": mensajesUsuario,})
        
        else:
            return render(request, "sistema/Vista_Conversacion.html", {
                "titulo": "Conversación General",
                "mensajes": MensajeDirecto.obtenerMensajesFiltrados(request.user),})

def plantel(request: HttpRequest):
    pass