from django.shortcuts import render
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from .forms_msj import MensajeDirectoForm
from .models_msj import MensajeDirecto
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse

from .models import UsuarioEscolar


def indice(request):
    return render(request, "sistema/Vista_Indice.html")

def iniciarSesion(request):
    if request.method == "POST":

        # Intentar iniciar sesión
        nombre_usuario = request.POST["nombre_usuario"]
        contrasena = request.POST["contrasena"]
        usuario = authenticate(request, username=nombre_usuario, password=contrasena)

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
    
def cerrarSesion(request):
    logout(request)
    return HttpResponseRedirect(reverse("indice"))

def registrarse(request):
    if request.method == "POST":
        nombre_usuario = request.POST["nombre_usuario"]
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
            usuario = UsuarioEscolar.objects.create_user(nombre_usuario, email, contrasena)
            usuario.save()
        except IntegrityError:
            return render(request, "sistema/Vista_Registrarse.html", {
                "mensaje": "Nombre de usuario ocupado."
            })
        login(request, usuario)
        return HttpResponseRedirect(reverse("indice"))
    else:
        return render(request, "sistema/Vista_Registrarse.html")
    
def servicioReportes(request):
    pass

def cocina(request):
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

def plantel(request):
    pass