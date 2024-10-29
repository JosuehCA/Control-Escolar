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


def index(request):
    return render(request, "sistema/index.html")

def login_view(request):
    if request.method == "POST":

        # Intentar iniciar sesión
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Validar usuario existente
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "sistema/login.html", {
                "message": "Nombre de usuario o contraseña incorrectos."
            })
    else:
        return render(request, "sistema/login.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Comparando contraseña confirmada
        password = request.POST["password"]   
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "sistema/register.html", {
                "message": "Las contraseñas no son iguales."
            })

        # Intentar crear usuario nuevo
        try:
            user = UsuarioEscolar.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "sistema/register.html", {
                "message": "Nombre de usuario ocupado."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "sistema/register.html")
    
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
                return redirect('servicioMensajeria')
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