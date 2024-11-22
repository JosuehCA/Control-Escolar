from django.shortcuts import render, redirect, get_object_or_404
from sistema.models.forms_plantel import *
from django.contrib import messages
from datetime import datetime
from sistema.models.models import *
from sistema.models.models_actividades import *
from sistema.forms_grupos import *

def creacionHorario(request):
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


def eliminacionHorario(request, horarioId):
    if request.method == "POST": 
        horarioEliminado = GestorHorarios.eliminarHorarioEscolar(horarioId)
        if horarioEliminado:
            messages.success(request, "Horario eliminado con éxito.")
        else:
            messages.error(request, "El horario no existe o ya ha sido eliminado.")
    return redirect('listaHorarios') 

def listaHorarios(request):
    listaHorarios = HorarioEscolar.objects.all()
    return render(request, "sistema/Vista_ListaHorarios.html", {'horarios': listaHorarios})


def creacionActividad(request):
    if request.method == "POST":
        crearActividadForm = CrearActividadForm(request.POST)
        if crearActividadForm.is_valid():
            horarioAsociado = crearActividadForm.cleaned_data['horario']
            nombreActividad = crearActividadForm.cleaned_data['nombre']
            descripcionActividad = crearActividadForm.cleaned_data['descripcion']
            horaInicioActividad = crearActividadForm.cleaned_data['horaInicio']
            horaFinalActividad = crearActividadForm.cleaned_data['horaFinal']
            fechaActividad = crearActividadForm.cleaned_data['fecha']
            grupoAsociado = crearActividadForm.cleaned_data['grupo']

            try:
                gestorActividades = GestorActividades()

                gestorActividades.agregarActividad(
                    horario=horarioAsociado,
                    nombre=nombreActividad,
                    descripcion=descripcionActividad,
                    horaInicio=horaInicioActividad,
                    horaFinal=horaFinalActividad,
                    fecha=fechaActividad,
                    grupo=grupoAsociado
                )
                messages.success(request, "Actividad agregada con éxito.")
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Formulario no válido.")
    else:
        crearActividadForm = CrearActividadForm()

    return render(request, 'sistema/Vista_CrearActividad.html', {'form': crearActividadForm})

def eliminacionActividad(request, actividadId):
    gestorActividades = GestorActividades()

    if gestorActividades.eliminarActividad(actividadId):
        return redirect("listaActividades")
    return render(request, "error.html", {"error": "No se pudo eliminar la actividad"})

def listaActividades(request):
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

def detallesDeActividad(request, actividadId):
    actividad = get_object_or_404(Actividad, id=actividadId)
    
    # Obtener todos los alumnos del grupo asociado
    grupo = actividad.grupo
    listaAlumnos = grupo.alumnos.all()

    # Verificar si algún alumno ya está participando en la actividad
    actividadIniciada = any(alumno.actividadActual == actividad for alumno in listaAlumnos)

    if request.method == "POST":
        # Si la actividad ya está asignada, cambiar a "terminada"
        if actividadIniciada:
            for alumno in listaAlumnos:
                if alumno.actividadActual == actividad:
                    alumno.actividadActual = None  # Terminar la actividad del alumno
                    alumno.save()
            actividadIniciada = False
        else:
            # Asignar la actividad a todos los alumnos del grupo
            for alumno in listaAlumnos:
                alumno.actividadActual = actividad
                alumno.save()
            actividadIniciada = True
        
        # Redirigir de nuevo a la página de detalles de la actividad
        return redirect('detallesDeActividad', actividadId=actividadId)

    return render(request, "sistema/Vista_DetallesActividad.html", {
        'actividad': actividad,
        'actividadIniciada': actividadIniciada,
        'alumnos': listaAlumnos
    })


def actualizacionActividad(request, actividadId):
    actividad = get_object_or_404(Actividad, id=actividadId)
    gestorActividades = GestorActividades()
    
    if request.method == "POST":
        actualizarActividadForm = ActualizarActividadForm(request.POST, instance=actividad)
        
        if actualizarActividadForm.is_valid():
            # Obtener los datos del formulario
            nombre = actualizarActividadForm.cleaned_data['nombre']
            descripcion = actualizarActividadForm.cleaned_data['descripcion']
            horaInicio = actualizarActividadForm.cleaned_data['horaInicio']
            horaFinal = actualizarActividadForm.cleaned_data['horaFinal']
            
            # Intentar actualizar la actividad con los nuevos datos
            try:
                if gestorActividades.actualizarActividad(
                    actividad=actividad,
                    nuevoNombre=nombre,
                    nuevaDescripcion=descripcion,
                    nuevaHoraInicio=horaInicio,
                    nuevaHoraFinal=horaFinal
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




#PASAR A OTRO LADO---------------------


def paseDeLista(request, grupoId):
    # Obtener el grupo
    grupo = get_object_or_404(Grupo, id=grupoId)
    paseDeListaForm = PaseDeListaForm(grupo)

    if request.method == 'POST':
        # Crear el formulario con los datos del POST
        paseDeListaForm = PaseDeListaForm(grupo, request.POST)

        if paseDeListaForm.is_valid():
            for alumno in grupo.alumnos.all():
                # Revisar si el formulario tiene marcada la asistencia
                if paseDeListaForm.cleaned_data.get(f'asistencias_{alumno.id}', False):
                    alumno.asistirAClase()  # Registrar asistencia
                else:
                    alumno.faltarAClase()  # Registrar falta
            return redirect('registroDeAsistencia', grupoId=grupo.id)

    return render(request, 'sistema/Vista_PaseDeLista.html', {'form': paseDeListaForm, 'grupo': grupo})



def registroDeAsistencia(request, grupoId):
    # Obtener el grupo
    grupo = get_object_or_404(Grupo, id=grupoId)
    fechaActual = date.today()

    # Obtener registros de asistencia del día
    listaAsistencias = RegistroAsistencia.objects.filter(
        alumno__in=grupo.alumnos.all(),
        fecha=fechaActual,
    )
    
    # Separar por asistencia y falta
    alumnosPresentes = [registro.alumno for registro in listaAsistencias if registro.asistencias] 
    alumnosAusentes = [registro.alumno for registro in listaAsistencias if not registro.asistencias]

    contexto = {
        'grupo': grupo,
        'alumnosPresentes': alumnosPresentes,
        'alumnosAusentes': alumnosAusentes,
        'fecha': fechaActual,
    }
    return render(request, 'sistema/Vista_RegistroDeAsistencias.html', contexto)
    

def asignacionCalificaciones(request, grupoId):
    grupo = get_object_or_404(Grupo, id=grupoId)
    listaAlumnos = Alumno.objects.filter(grupo=grupo)
    rangoDecalificaciones = range(1, 6)  

    if request.method == "POST":
        for alumno in listaAlumnos:
            calificacion = request.POST.get(f"calificacion_{alumno.id}")
            comentario = request.POST.get(f"comentario_{alumno.id}")
            
            if calificacion:
                RegistroCalificaciones.objects.update_or_create(
                    alumno=alumno,
                    grupo=grupo,
                    fecha=date.today(),
                    defaults={
                        "calificacion": int(calificacion),
                        "comentario": comentario or "",
                    }
                )
        return redirect("registroDeAsistencia", grupoId=grupo.id)

    return render(request, "sistema/Vista_AsignarCalificaciones.html", {
        "grupo": grupo,
        "alumnos": listaAlumnos,
        "calificaciones": rangoDecalificaciones
    })
