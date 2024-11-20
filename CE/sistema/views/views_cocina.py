from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from sistema.models.models import Platillo, MenuSemanal, Nutricionista

def opcionesMenu(request):
    return render(request, "sistema/opcionesMenu.html")

def obtenerInformacionCreacionPlatillo(request): #Pendiente nombre
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        consideraciones = request.POST.get("consideraciones")

        Nutricionista.crearRecomendaciones(nombre, descripcion, consideraciones)
        
        return redirect("opcionesMenu")
    
    return render(request, "sistema/crearPlatillo.html")

def obtenerInformacionCreacionMenu(request): #Pendiente nombre
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")
        
        Nutricionista.crearMenuSemanal(nombre, fecha_inicio, fecha_fin)

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


def obtenerInformacionAgregarPlatillo(request, menu_id): #pendiente nombre (agregarPlatillo)
    menu = get_object_or_404(MenuSemanal, id=menu_id)
    dia = request.GET.get('dia')
    platillos = Platillo.objects.all() 
    
    if request.method == "POST":
        platillo_id = request.POST.get('platillo_id')
        menu.agregarPlatillo(platillo_id, dia)  # Llama al método del modelo para manejar la lógica
        return redirect('gestionarMenuSemanal', menu_id=menu.id)

    return render(request, 'sistema/accionPlatillo.html', {
        'accion': 'add',
        'menu': menu,
        'platillos': platillos,
        'dia': dia,
    })



def obtenerInformacionModificarPlatillo(request, menu_id): #pendiente nombre y funcionalidad (editarPlatillo)
    # Obtener el menú
    menu = get_object_or_404(MenuSemanal, id=menu_id)
    
    # Obtener el día desde los parámetros GET
    dia = request.GET.get('dia')
    
    # Obtener todos los platillos para ese menú y día
    platillos = Platillo.objects.filter(menu=menu, dia=dia)
    
    # Obtener una instancia del Nutricionista
    nutricionista = Nutricionista.objects.first()  # PENDIENTE
    
    # Si es una solicitud POST, actualizar el platillo
    if request.method == 'POST':
        platillo_id = request.POST.get('platillo_id')
        
        # Llamar al método editarPlatillo del modelo Nutricionista
        nutricionista.modificarRecomendaciones(
            platillo_id=platillo_id,
            nombre=request.POST.get('nombre'),
            descripcion=request.POST.get('descripcion'),
            consideraciones=request.POST.get('consideraciones')
        )

        return redirect('gestionarMenuSemanal', menu_id=menu.id)
    
    return render(request, 'sistema/accionPlatillo.html', {
        'accion': 'edit',
        'menu': menu,
        'platillos': platillos,
        'dia': dia,
    })



def obtenerInformacionEliminarPlatillo(request, menu_id):  # Pendiente nombre (eliminarPlatillo)
    # Obtener el menú desde la base de datos
    menu = get_object_or_404(MenuSemanal, id=menu_id)

    # Obtener el día desde los parámetros GET
    dia = request.GET.get('dia')

    # Obtener todos los platillos asociados al menú y al día
    platillos = Platillo.objects.filter(menu=menu, dia=dia)

    if request.method == 'POST':
        # Obtener el ID del platillo a eliminar desde el formulario
        platillo_id = request.POST.get('platillo_id')

        # Delegar al modelo la lógica de eliminación
        menu.eliminarPlatillo(platillo_id, dia)

        return redirect('gestionarMenuSemanal', menu_id=menu.id)

    # Renderizar la página de acción con los datos necesarios
    return render(request, 'sistema/accionPlatillo.html', {
        'accion': 'delete',
        'menu': menu,
        'platillos': platillos,
        'dia': dia,
    })



def eliminarMenu(request, menu_id): #pendiente nombre
    # Llamar al método de Nutricionista para eliminar el menú
    Nutricionista.eliminarMenuSemanal(menu_id)
    
    # Redirigir a otra página después de eliminar el menú
    return redirect('seleccionarMenuSemanal')