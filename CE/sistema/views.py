from django.shortcuts import render
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from .models import UsuarioEscolar

<<<<<<< Updated upstream
# Create your views here.
=======
from .forms import *
from django.shortcuts import render, redirect
from .models import *



>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
        return render(request, "sistema/register.html")
=======
        return render(request, "sistema/register.html")
    
def crear_horario(request):
    if request.method == "POST":
        form = CrearHorarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('actividades')  
    else:
        form = CrearHorarioForm()

    return render(request, "sistema/crear_horario.html", {'form': form})


def crear_actividad(request):
    if request.method == 'POST':
        form = ActividadForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('lista_actividades') 
    else:
        form = ActividadForm()
    return render(request, "sistema/crear_actividad.html", {'form': form})


def eliminar_actividad(request, actividad_id):
    """Elimina una actividad específica."""
    actividad = get_object_or_404(Actividad, id=actividad_id)
    actividad.delete()
    return HttpResponseRedirect(reverse('lista_actividades'))

def listar_actividades(request):
    actividades = Actividad.objects.all()
    fecha = None

    if request.method == "POST":
        fecha = request.POST.get('fecha')
        if fecha:
            fecha = timezone.datetime.strptime(fecha, '%Y-%m-%d').date()
            horario = HorarioDeActividades.objects.filter(fecha=fecha).first()
            if horario:
                actividades = horario.actividades.all()
            else:
                actividades = [] 

    return render(request, "sistema/listar_actividades.html", {'actividades': actividades, 'fecha': fecha})

    
def servicioReportes(request):
    pass

def cocina(request):
    pass

def mensajeria(request):
    pass

def plantel(request):
    pass
>>>>>>> Stashed changes
