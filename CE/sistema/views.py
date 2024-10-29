from django.shortcuts import render
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect

from .models import UsuarioEscolar
from .models import Alumno, Grupo, Administrador, Profesor

# Create your views here.

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
    
def administrar(request):
    return render(request, "sistema/administrar.html")
    
def crearGrupo(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        alumnosIds = request.POST.getlist('alumnos')
        alumnos = Alumno.objects.filter(id__in=alumnosIds)
        
        # Crear el grupo sin restricción de rol
        nuevo_grupo = Grupo(nombre=nombre)
        nuevo_grupo.save()
        nuevo_grupo.alumnos.set(alumnos)
        nuevo_grupo.save()

        # Redirige para evitar que se reenvíe el formulario al refrescar la página
        return render(request, "sistema/crearGrupo.html")
      # Asegúrate de tener el nombre de la URL correcta

    # Obtener todos los grupos para mostrarlos en la plantilla
    grupos = Grupo.objects.all()
    alumnos = Alumno.objects.all()
    return render(request, "sistema/crearGrupo.html", {
        'alumnos': alumnos,
        'grupos': grupos
    })
    
    
def eliminarGrupo(request, grupo_id):
    administrador = request.user

    # Eliminar el grupo usando el método del administrador
    administrador.eliminarGrupo(grupo_id)

    return render(request, "sistema/crearGrupo.html")


