from django.shortcuts import render, redirect, get_object_or_404
from sistema.models.forms_plantel import *
from django.contrib import messages
from datetime import datetime
from sistema.models.models import *
from django.views import View


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
            grupo = crearActividadForm.cleaned_data['grupo']

            try:
                # Intenta agregar la actividad, la validación se hace dentro de agregarActividad
                gestorActividades = GestorActividades()

                gestorActividades.agregarActividad(
                    horario=horario,
                    nombre=nombre,
                    descripcion=descripcion,
                    horaInicio=hora_inicio,
                    horaFinal=hora_final,
                    fecha=fecha,
                    grupo=grupo
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
    
    # Obtener todos los alumnos del grupo asociado
    grupo = actividad.grupo
    alumnos = grupo.alumnos.all()

    # Verificar si algún alumno ya está participando en la actividad
    actividad_iniciada = any(alumno.actividadActual == actividad for alumno in alumnos)

    if request.method == "POST":
        # Si la actividad ya está asignada, cambiar a "terminada"
        if actividad_iniciada:
            for alumno in alumnos:
                if alumno.actividadActual == actividad:
                    alumno.actividadActual = None  # Terminar la actividad del alumno
                    alumno.save()
            actividad_iniciada = False
        else:
            # Asignar la actividad a todos los alumnos del grupo
            for alumno in alumnos:
                alumno.actividadActual = actividad
                alumno.save()
            actividad_iniciada = True
        
        # Redirigir de nuevo a la página de detalles de la actividad
        return redirect('detalle_actividad', id=id)

    return render(request, "sistema/Vista_DetallesActividad.html", {
        'actividad': actividad,
        'actividad_iniciada': actividad_iniciada,
        'alumnos': alumnos
    })


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




#PASAR A OTRO LADO

class PaseDeListaView(View):
    template_name = 'sistema/pase_de_lista.html'

    def get(self, request, grupo_id):
        # Obtener el grupo
        grupo = get_object_or_404(Grupo, id=grupo_id)
        form = PaseDeListaForm(grupo)
        return render(request, self.template_name, {'form': form, 'grupo': grupo})

    def post(self, request, grupo_id):
        # Obtener el grupo
        grupo = get_object_or_404(Grupo, id=grupo_id)
        form = PaseDeListaForm(grupo, request.POST)

        if form.is_valid():
            for alumno in grupo.alumnos.all():
                # Revisar si el formulario tiene marcada la asistencia
                if form.cleaned_data.get(f'asistencias_{alumno.id}', False):
                    alumno.asistirAClase()  # Registrar asistencia
                else:
                    alumno.faltarAClase()  # Registrar falta
            return redirect('grupo_detalle', grupo_id=grupo.id)

        return render(request, self.template_name, {'form': form, 'grupo': grupo})

class GrupoDetalleView(View):
    template_name = 'sistema/detalle.html'

    def get(self, request, grupo_id):
        grupo = get_object_or_404(Grupo, id=grupo_id)
        hoy = date.today()

        # Obtener registros de asistencia del día
        asistencias = RegistroAsistencia.objects.filter(
            alumno__in=grupo.alumnos.all(),
            fecha=hoy,
        )
        
        # Separar por asistencia y falta
        alumnos_asistieron = [registro.alumno for registro in asistencias if registro.asistencias] #le movi a registro.asistencia
        alumnos_faltaron = [registro.alumno for registro in asistencias if not registro.asistencias]

        contexto = {
            'grupo': grupo,
            'alumnos_asistieron': alumnos_asistieron,
            'alumnos_faltaron': alumnos_faltaron,
            'fecha': hoy,
        }
        return render(request, self.template_name, contexto)
    

def asignar_calificaciones(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)
    alumnos = Alumno.objects.filter(grupo=grupo)
    calificaciones = range(1, 6)  # Generar los números del 1 al 5

    if request.method == "POST":
        for alumno in alumnos:
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
        return redirect("detalle_grupo", grupo_id=grupo.id)

    return render(request, "sistema/asignar_calificaciones.html", {
        "grupo": grupo,
        "alumnos": alumnos,
        "calificaciones": calificaciones
    })
