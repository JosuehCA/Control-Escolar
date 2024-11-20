from django.shortcuts import render, redirect, get_object_or_404
from sistema.models.forms_plantel import *
from django.contrib import messages
from datetime import datetime

from sistema.models.models_actividades import *

def crear_horario(request):
    if request.method == "POST":
        crearHorarioForm = CrearHorarioForm(request.POST)
        if crearHorarioForm.is_valid():
            try:
                fecha = crearHorarioForm.cleaned_data['fecha']
                horaEntrada = crearHorarioForm.cleaned_data['horaEntrada']
                horaSalida = crearHorarioForm.cleaned_data['horaSalida']
                
                GestorHorarios.crearHorarioEscolar(fecha, horaEntrada, horaSalida)
                messages.success(request, "Horario creado con éxito")
            except Exception as e:
                messages.error(request, f"Hubo un error al crear el horario: {str(e)}")
        else:
            for error in crearHorarioForm.errors.values():
                messages.error(request, error)
    else:
        crearHorarioForm = CrearHorarioForm()

    return render(request, "sistema/Vista_CrearHorario.html", {'form': crearHorarioForm})


def eliminar_horario(request, horario_id):
    if request.method == "POST": 
        horarioEliminado = GestorHorarios.eliminarHorarioEscolar(horario_id)
        if horarioEliminado:
            messages.success(request, "Horario eliminado con éxito.")
        else:
            messages.error(request, "El horario no existe o ya ha sido eliminado.")
    return redirect('lista_horarios') 

def listar_horarios(request):
    listaHorarios = HorarioEscolar.objects.all()
    return render(request, "sistema/Vista_ListaHorarios.html", {'horarios': listaHorarios})


def crear_actividad(request):
    if request.method == "POST":
        crearActividadForm = CrearActividadForm(request.POST)
        if crearActividadForm.is_valid():
            horario = crearActividadForm.cleaned_data['horario']
            nombre = crearActividadForm.cleaned_data['nombre']
            descripcion = crearActividadForm.cleaned_data['descripcion']
            hora_inicio = crearActividadForm.cleaned_data['horaInicio']
            hora_final = crearActividadForm.cleaned_data['horaFinal']
            fecha = crearActividadForm.cleaned_data['fecha']

            try:
                # Intenta agregar la actividad, la validación se hace dentro de agregarActividad
                gestorActividades = GestorActividades()

                gestorActividades.agregarActividad(
                    horario=horario,
                    nombre=nombre,
                    descripcion=descripcion,
                    horaInicio=hora_inicio,
                    horaFinal=hora_final,
                    fecha=fecha
                )
                messages.success(request, "Actividad agregada con éxito.")
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Formulario no válido.")
    else:
        crearActividadForm = CrearActividadForm()

    return render(request, 'sistema/Vista_CrearActividad.html', {'form': crearActividadForm})

def eliminar_actividad(request, actividad_id):
    gestorActividades = GestorActividades()

    if gestorActividades.eliminarActividad(actividad_id):
        return redirect("lista_actividades")
    return render(request, "error.html", {"error": "No se pudo eliminar la actividad"})

def listar_actividades(request):
    fecha = request.GET.get('fecha', None)
    if fecha:
        try:
            gestorActividades = GestorActividades()
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
            listaActividades = gestorActividades.filtrarActividadesPorFecha(fecha_obj)
        except ValueError:
            listaActividades = Actividad.objects.all()
    else:
        listaActividades = Actividad.objects.all()

    return render(request, "sistema/Vista_ListaActividades.html", {
        "actividades": listaActividades,
        "fecha": fecha  
    })

def detalle_actividad(request, id):
    actividad = get_object_or_404(Actividad, id=id)
    return render(request, "sistema/Vista_DetallesActividad.html", {'actividad': actividad})

def actualizar_actividad(request, actividad_id):
    actividad = get_object_or_404(Actividad, id=actividad_id)
    gestor_actividades = GestorActividades()
    
    if request.method == "POST":
        actualizarActividadForm = ActualizarActividadForm(request.POST, instance=actividad)
        
        if actualizarActividadForm.is_valid():
            # Obtener los datos del formulario
            nombre = actualizarActividadForm.cleaned_data['nombre']
            descripcion = actualizarActividadForm.cleaned_data['descripcion']
            hora_Inicio = actualizarActividadForm.cleaned_data['horaInicio']
            hora_Final = actualizarActividadForm.cleaned_data['horaFinal']
            
            # Intentar actualizar la actividad con los nuevos datos
            try:
                if gestor_actividades.actualizarActividad(
                    actividad=actividad,
                    nombre=nombre,
                    descripcion=descripcion,
                    horaInicio=hora_Inicio,
                    horaFinal=hora_Final
                ):
                    # Si se actualizó, redirigir a la lista de actividades
                    messages.success(request, "Actividad actualizada con éxito.")
                    return render(request, 'sistema/Vista_ActualizarActividad.html', {'form': actualizarActividadForm, 'actividad': actividad, 'redirect': True})
                else:
                    actualizarActividadForm.add_error(None, "No se realizaron cambios en la actividad.")
            except ValueError as e:
                actualizarActividadForm.add_error(None, str(e))
        else:
            pass
    else:
        actualizarActividadForm = ActualizarActividadForm(instance=actividad)

    return render(request, 'sistema/Vista_ActualizarActividad.html', {'form': actualizarActividadForm, 'actividad': actividad})
