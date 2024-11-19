from django.shortcuts import render
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from .models import UsuarioEscolar
from .models import Alumno, Grupo, Administrador, Profesor, Nutricionista
from .models import Platillo, MenuSemanal
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
    
def administrarGrupos(request):
    if request.method == 'POST':
        action = request.POST.get('action', 'create')  # Obtén la acción del formulario

        if action == 'create':  # Crear un nuevo grupo
            nombre = request.POST.get('nombre')
            alumnosIds = request.POST.getlist('alumnos')
            alumnos = Alumno.objects.filter(id__in=alumnosIds)
            
            if not Administrador.alumnosNoTienenGrupo(alumnos):
                print("Alguno de los alumnos ya pertenece a un grupo.")
            else:
                Administrador.crearGrupo(nombre, list(alumnos))

        elif action == 'delete':  # Eliminar grupos seleccionados
            gruposIds = request.POST.getlist('grupos')
            for grupoId in gruposIds:
                try:
                    grupo = Grupo.objects.get(id=grupoId)
                    grupo.delete()
                except Grupo.DoesNotExist:
                    print(f"Grupo con ID {grupoId} no existe.")
                    
        elif action == 'edit':
            grupoId = request.POST.get('grupo_id')
            nombre = request.POST.get('nombre')
            alumnosIds = request.POST.getlist('alumnos')
            alumnos = Alumno.objects.filter(id__in=alumnosIds)
            
            try:
                
                gruposActuales = Grupo.objects.filter(alumnos__in=alumnos)
                for grupo in gruposActuales:
                    grupo.alumnos.remove(*alumnos)
                
                if not Administrador.alumnosNoTienenGrupo(alumnos):
                    print("Alguno de los alumnos ya pertenece a un grupo.")
                else:
                    Administrador.editarGrupo(grupoId, nombre, list(alumnos))
            except Grupo.DoesNotExist:
                print(f"Grupo con ID {grupoId} no existe.")

        # Redirige para evitar que se reenvíe el formulario al refrescar la página
        return redirect("administrarGrupos")

    # Obtener todos los grupos y alumnos para mostrarlos en la plantilla
    grupos = Grupo.objects.all()
    alumnos = Alumno.objects.all()
    return render(request, "sistema/administrarGrupos.html", {
        'alumnos': alumnos,
        'grupos': grupos
    })

def opcionesMenu(request):
    return render(request, "sistema/opcionesMenu.html")

def crearPlatillo(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        consideraciones = request.POST.get("consideraciones")
        
        Platillo.objects.create(
            nombre=nombre, 
            descripcion=descripcion, 
            consideraciones=consideraciones
        )
        return redirect("opcionesMenu")
    
    return render(request, "sistema/crearPlatillo.html")

def crearMenuSemanal(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")
        
        MenuSemanal.objects.create(
            nombre=nombre, 
            fecha_inicio=fecha_inicio, 
            fecha_fin=fecha_fin
        )
        return redirect("opcionesMenu")
    
    return render(request, "sistema/crearMenuSemanal.html")

def seleccionarMenuSemanal(request):
    # Verificar si se ha pasado el `menu_id` a través de los parámetros GET
    menu_id = request.GET.get('menu_id')
    if menu_id:
        # Si se ha seleccionado un menú, verificar si se va a 'ver' o 'gestionar'
        if request.GET.get('ver'):
            return verMenuSemanal(request, menu_id)
        else:
            return gestionarMenuSemanal(request, menu_id)

    # Si no se ha seleccionado un menú, simplemente renderizar el formulario con todos los menús
    menus = MenuSemanal.objects.all()
    return render(request, "sistema/seleccionarMenuSemanal.html", {
        'menus': menus
    })
        
def verMenuSemanal(request, menu_id):
    try:
        # Obtener el menú seleccionado
        menu = MenuSemanal.objects.get(id=menu_id)

        # Obtener todos los platillos relacionados con este menú
        platillos = Platillo.objects.filter(menu=menu)
        
        # Organizar los platillos por día de la semana
        platillos_por_dia = {dia: [] for dia in ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']}

        # Agregar los platillos a los días correspondientes
        for platillo in platillos:
            platillos_por_dia[platillo.dia].append(platillo)

        return render(request, 'sistema/verMenuSemanal.html', {
            'menu': menu,
            'platillos_por_dia': platillos_por_dia,
        })
    except MenuSemanal.DoesNotExist:
        return render(request, 'sistema/error.html', {'message': 'Menú no encontrado.'}) 


def gestionarMenuSemanal(request, menu_id):
    menu = get_object_or_404(MenuSemanal, id=menu_id)
    platillos_por_dia = {}

    # Obtener los platillos del menú organizados por día
    dias_de_la_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    for dia in dias_de_la_semana:
        platillos_por_dia[dia] = Platillo.objects.filter(menu=menu, dia=dia)

    # Pasar el diccionario de platillos por día de manera directa
    return render(request, 'sistema/gestionarMenuSemanal.html', {
        'menu': menu,
        'dias': dias_de_la_semana,
        'platillos_por_dia': platillos_por_dia.items(),  # Pasar como items() de un diccionario
    })


def agregarPlatillo(request, menu_id):
    menu = get_object_or_404(MenuSemanal, id=menu_id)
    dia = request.GET.get('dia')
    platillos = Platillo.objects.all()  # PEND: Aplicar filtros si se quiere limitar los platillos mostrados
    
    if request.method == "POST":
        platillo_id = request.POST.get('platillo_id')
        platillo = get_object_or_404(Platillo, id=platillo_id)
        platillo.menu = menu
        platillo.dia = dia
        platillo.save()
        return redirect('gestionarMenuSemanal', menu_id=menu.id)

    return render(request, 'sistema/accionPlatillo.html', {
        'accion': 'add',
        'menu': menu,
        'platillos': platillos,
        'dia': dia,
    })


def editarPlatillo(request, menu_id):
    # Obtener el menú
    menu = get_object_or_404(MenuSemanal, id=menu_id)
    
    # Obtener el día desde los parámetros GET
    dia = request.GET.get('dia')  # Día del menú para el cual se editará el platillo
    
    # Obtener todos los platillos para ese menú y día
    platillos = Platillo.objects.filter(menu=menu, dia=dia)
    
    # Si es una solicitud POST, actualizar el platillo
    if request.method == 'POST':
        platillo_id = request.POST.get('platillo_id')  # Obtener el platillo a editar
        platillo = get_object_or_404(Platillo, id=platillo_id)

        # Actualizar los campos del platillo
        platillo.nombre = request.POST.get('nombre')
        platillo.descripcion = request.POST.get('descripcion')
        platillo.consideraciones = request.POST.get('consideraciones')
        platillo.save()

        return redirect('gestionarMenuSemanal', menu_id=menu.id)
    
    # Si es una solicitud GET, mostrar los platillos de ese día para que se seleccione el que desea editar
    return render(request, 'sistema/accionPlatillo.html', {
        'accion': 'edit',
        'menu': menu,
        'platillos': platillos,  # Mostrar platillos del día
        'dia': dia,  # Pasar el día para saber de qué menú se trata
    })


def eliminarPlatillo(request, menu_id):
    # Obtener el menú
    menu = get_object_or_404(MenuSemanal, id=menu_id)
    
    # Obtener el día desde los parámetros GET
    dia = request.GET.get('dia')  # Día del menú para el cual se eliminará el platillo
    
    # Obtener todos los platillos para ese menú y día
    platillos = Platillo.objects.filter(menu=menu, dia=dia)

    # Si es una solicitud POST, eliminar el platillo seleccionado
    if request.method == 'POST':
        platillo_id = request.POST.get('platillo_id')  # Obtener el platillo a eliminar
        platillo = get_object_or_404(Platillo, id=platillo_id)

        # Desasociar el platillo del menú (lo elimina del día)
        platillo.menu = None
        platillo.dia = None
        platillo.save()

        return redirect('gestionarMenuSemanal', menu_id=menu.id)

    # Si es una solicitud GET, mostrar los platillos de ese día para que se seleccione el que desea eliminar
    return render(request, 'sistema/accionPlatillo.html', {
        'accion': 'delete',
        'menu': menu,
        'platillos': platillos,  # Mostrar platillos del día
        'dia': dia,  # Pasar el día para saber de qué menú se trata
    })


def eliminarMenu(request, menu_id):
    # Asegurarse de que el menú existe
    menu = get_object_or_404(MenuSemanal, id=menu_id)
    
    # Eliminar el menú
    menu.delete()
    
    # Redirigir a otra página después de eliminar el menú
    return redirect('seleccionarMenuSemanal')
