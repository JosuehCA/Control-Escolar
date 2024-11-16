from django.shortcuts import render
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect

from .models import UsuarioEscolar
from .models import Alumno, Grupo, Administrador, Profesor
from django.shortcuts import get_object_or_404

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
    
from django.shortcuts import redirect

def administrarGrupos(request):
    if request.method == 'POST':
        action = request.POST.get('action', 'create')  # Obtén la acción del formulario

        if action == 'create':  # Crear un nuevo grupo
            nombre = request.POST.get('nombre')
            alumnosIds = request.POST.getlist('alumnos')
            alumnos = Alumno.objects.filter(id__in=alumnosIds)

            Administrador.crearGrupo(nombre, list(alumnos))

        elif action == 'delete':  # Eliminar grupos seleccionados
            gruposIds = request.POST.getlist('grupos')
            for grupo_id in gruposIds:
                try:
                    grupo = Grupo.objects.get(id=grupo_id)
                    grupo.delete()
                except Grupo.DoesNotExist:
                    print(f"Grupo con ID {grupo_id} no existe.")
                    
        elif action == 'edit':
            grupo_id = request.POST.get('grupo_id')
            nombre = request.POST.get('nombre')
            alumnosIds = request.POST.getlist('alumnos')
            alumnos = Alumno.objects.filter(id__in=alumnosIds)
            try:
                Administrador.editarGrupo(grupo_id, nombre, list(alumnos))
            except Grupo.DoesNotExist:
                print(f"Grupo con ID {grupo_id} no existe.")

        # Redirige para evitar que se reenvíe el formulario al refrescar la página
        return redirect("administrarGrupos")

    # Obtener todos los grupos y alumnos para mostrarlos en la plantilla
    grupos = Grupo.objects.all()
    alumnos = Alumno.objects.all()
    return render(request, "sistema/administrarGrupos.html", {
        'alumnos': alumnos,
        'grupos': grupos
    })