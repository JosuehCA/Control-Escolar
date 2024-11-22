from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404 
from django.contrib import messages

from sistema.models.models import Chef, Platillo, MenuSemanal, Nutricionista, MenuPlatillo

def opcionesMenu(request):
    return render(request, "sistema/Vista_OpcionesMenu.html")

def gestionarRecomendaciones(request):
    platillos = Platillo.objects.all() 
    return render(request, "sistema/Vista_GestionarRecomendaciones.html", {'platillos': platillos})

def crearRecomendacion(request):
    if request.method == "POST":
        
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        consideraciones = request.POST.get("consideraciones")
        
        try:
            Platillo.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                consideraciones=consideraciones
            )
            
            messages.success(request, "Recomendación creada con éxito.")
            return redirect("gestionarRecomendaciones")  
        except Exception as e:
            messages.error(request, f"Ocurrió un error: {e}")
            return redirect("crearRecomendacion")  
    
    return render(request, "sistema/Vista_CrearRecomendacion.html")

def editarRecomendacion(request, platillo_id):
   
    platillo = get_object_or_404(Platillo, id=platillo_id) 

    if request.method == "POST":
        
        platillo.nombre = request.POST.get("nombre")
        platillo.descripcion = request.POST.get("descripcion")
        platillo.consideraciones = request.POST.get("consideraciones")
        
        
        try:
            platillo.save()
            messages.success(request, "Recomendación actualizada con éxito.")
            return redirect("gestionarRecomendaciones")  
        except Exception as e:
            messages.error(request, f"Ocurrió un error al actualizar: {e}")
            return render(request, "sistema/Vista_EditarRecomendacion.html", {"recomendacion": platillo})
    
    return render(request, "sistema/Vista_EditarRecomendacion.html", {"recomendacion": platillo})

def eliminarRecomendacion(request, platillo_id):
    
    platillo = get_object_or_404(Platillo, id=platillo_id)
    
    if request.method == "POST":
        try:
            platillo.delete()
            messages.success(request, "Recomendación eliminada con éxito.")
            return redirect("gestionarRecomendaciones") 
        except Exception as e:
            messages.error(request, f"Ocurrió un error: {e}")
            return render(request, "sistema/error.html", {"message": str(e)})
    
    return render(request, "sistema/Vista_GestionarRecomendaciones.html")

def crearMenu(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")
        
        try:
            Chef.crearMenuSemanal(nombre, fecha_inicio, fecha_fin)
            messages.success(request, "Menú semanal creado con éxito.")
        except Exception as e:
            messages.error(request, f"Error al crear el menú: {str(e)}")
        return redirect("opcionesMenu")
    
    return render(request, "sistema/Vista_CrearMenuSemanal.html")


def seleccionarMenuSemanal(request):
    menu_id = request.GET.get('menu_id')
    if menu_id:
        if request.GET.get('ver'):
            return vizualizarMenuSemanal(request, menu_id)
        else:
            return gestionarMenuSemanal(request, menu_id)

    menus = MenuSemanal.objects.all()
    return render(request, "sistema/Vista_SeleccionarMenuSemanal.html", {
        'menus': menus
    })

        
def vizualizarMenuSemanal(request, menu_id):
    try:
        menu = MenuSemanal.objects.get(id=menu_id)

        platillosPorDia = {dia: [] for dia in ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']}

        menu_platillos = MenuPlatillo.objects.filter(menu=menu)

        for menu_platillo in menu_platillos:
            platillosPorDia[menu_platillo.dia].append(menu_platillo.platillo)

        return render(request, 'sistema/Vista_VerMenuSemanal.html', {
            'menu': menu,
            'platillos_por_dia': platillosPorDia,
        })
    except MenuSemanal.DoesNotExist:
        messages.error(request, "El menú solicitado no existe.")
        return redirect("seleccionarMenuSemanal")



def gestionarMenuSemanal(request, menu_id): 
    menu = get_object_or_404(MenuSemanal, id=menu_id)
    platillosPorDia = {}

    diasDeLaSemana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    for dia in diasDeLaSemana:
        platillosPorDia[dia] = Platillo.objects.filter(platillo_menus__menu=menu, platillo_menus__dia=dia)

    return render(request, 'sistema/Vista_GestionarMenuSemanal.html', {
        'menu': menu,
        'dias': diasDeLaSemana,
        'platillos_por_dia': platillosPorDia.items(),
    })


def agregarPlatilloDelDia(request, menu_id):
    menu = get_object_or_404(MenuSemanal, id=menu_id)
    dia = request.GET.get('dia')
    platillos = Platillo.objects.all()

    if request.method == "POST":
        platillo_id = request.POST.get('platillo_id')
        try:
            Chef.agregarPlatilloAlMenu(menu, platillo_id, dia)
            messages.success(request, "Platillo agregado con éxito.")
        except Exception as e:
            messages.error(request, f"Error al agregar el platillo: {str(e)}")
        return redirect('gestionarMenuSemanal', menu_id=menu.id)

    return render(request, 'sistema/Vista_AccionPlatillo.html', {
        'accion': 'add',
        'menu': menu,
        'platillos': platillos,
        'dia': dia,
    })


def modificarPlatilloDelDia(request, menu_id): 
    menu = get_object_or_404(MenuSemanal, id=menu_id)
    dia = request.GET.get('dia')

    platillos = Platillo.objects.filter(platillo_menus__menu=menu, platillo_menus__dia=dia)

    if request.method == 'POST':
        platillo_id = request.POST.get('platillo_id')
        try:
            Nutricionista.modificarRecomendaciones(
                menu,
                platillo_id=platillo_id,
                nombre=request.POST.get('nombre'),
                descripcion=request.POST.get('descripcion'),
                consideraciones=request.POST.get('consideraciones')
            )
            messages.success(request, "Recomendación modificada con éxito.")
            return redirect('gestionarMenuSemanal', menu_id=menu.id)
        except Exception as e:
            messages.error(request, f"Error al modificar la recomendación: {str(e)}")
            return redirect('gestionarMenuSemanal', menu_id=menu.id)

    return render(request, 'sistema/Vista_AccionPlatillo.html', {
        'accion': 'edit',
        'menu': menu,
        'platillos': platillos,
        'dia': dia,
    })


def eliminarPlatilloDelDia(request, menu_id):  
    menu = get_object_or_404(MenuSemanal, id=menu_id)
    dia = request.GET.get('dia')
    platillos = Platillo.objects.filter(platillo_menus__menu=menu, platillo_menus__dia=dia)

    if request.method == 'POST':
        platillo_id = request.POST.get('platillo_id')
        try:
            
            Chef.eliminarPlatilloDelMenu(menu, platillo_id, dia) 
            messages.success(request, "Platillo eliminado con éxito.")
            return redirect('gestionarMenuSemanal', menu_id=menu.id)
        except Exception as e:
            messages.error(request, f"Error al eliminar el platillo: {str(e)}")
            return redirect('gestionarMenuSemanal', menu_id=menu.id)

    return render(request, 'sistema/Vista_AccionPlatillo.html', {
        'accion': 'delete',
        'menu': menu,
        'platillos': platillos,
        'dia': dia,
    })


def eliminarMenu(request, menu_id): 
    Chef.eliminarMenuSemanal(menu_id)

    return redirect('seleccionarMenuSemanal')