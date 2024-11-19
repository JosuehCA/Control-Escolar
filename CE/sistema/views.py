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


from .models import Alumno, Grupo, Administrador, Platillo, MenuSemanal, UsuarioEscolar
from django.shortcuts import get_object_or_404
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
