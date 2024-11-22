from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect

from sistema.forms_usuarios import CrearUsuarioForm, EliminarUsuarioForm, ModificarUsuarioForm
from sistema.models.models import GestorDeUsuarios, Alumno, Grupo, GestorDeGrupos, Profesor, Tutor, UsuarioEscolar
from django.shortcuts import redirect
from sistema.forms_grupos import ActualizarGrupoForm, CrearGrupoForm

def administrar(request):
    return render(request, "sistema/Vista_Administrador.html")

def administrarGrupo(request):
    return render(request, "sistema/Vista_AdministrarGrupos.html")
    
def crearGrupo(request):
    if request.method == 'POST':
        form = CrearGrupoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            alumnos = form.cleaned_data['alumnos']

            if alumnos.count() == 0:
                messages.error(request, "No se puede crear un grupo sin alumnos.")
                return redirect('crearGrupo')

            # Crear grupo usando el gestor
            if GestorDeGrupos.crearGrupo(nombre, list(alumnos)):
                messages.success(request, "Grupo creado con éxito.")
                return redirect('crearGrupo')
            else:
                messages.error(request, "Error al crear el grupo.")
    else:
        form = CrearGrupoForm()

    return render(request, 'sistema/Vista_CrearGrupo.html', {'form': form})

    
def eliminarGrupo(request, grupoId):
    if GestorDeGrupos.eliminarGrupo(grupoId):
        messages.success(request, "Grupo eliminado con éxito.")
        return redirect('listaGrupos')
    else:
        messages.error(request, "Error al eliminar el grupo.")
    
    grupos = Grupo.objects.prefetch_related('alumnos').all()
    return render(request, "sistema/Vista_ListaGrupos.html", {'grupos': grupos})

    
def modificarGrupo(request, grupoId):
    grupo = get_object_or_404(Grupo, id=grupoId)

    if request.method == "POST":
        form = ActualizarGrupoForm(request.POST, instance=grupo)

        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            alumnos = form.cleaned_data['alumnos']

            try:
                cambios = GestorDeGrupos.modificarGrupo(grupo_id=grupoId, nombre=nombre, alumnos=list(alumnos))
                if cambios:
                    messages.success(request, "Grupo actualizado con éxito.")
                else:
                    messages.info(request, "No se realizaron cambios.")
                return redirect('listaGrupos')
            except ValueError as e:
                form.add_error(None, str(e))
    else:
        form = ActualizarGrupoForm(instance=grupo)

    return render(request, 'sistema/Vista_ModificarGrupo.html', {'form': form, 'grupo': grupo})


    
def listar_grupos(request):
    grupos = Grupo.objects.prefetch_related('alumnos').all()
    return render(request, "sistema/Vista_ListaGrupos.html", {'grupos': grupos})


def crearUsuario(request):
    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            # Obtener datos del formulario
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            username = form.cleaned_data['username']
            contrasena = form.cleaned_data['contrasena']
            rol = form.cleaned_data['rol']
            grupo = form.cleaned_data.get('grupo')
            tutor = form.cleaned_data.get('tutor')

            # Llamar al método para crear el usuario
            try:
                GestorDeUsuarios.crearUsuarioEscolar(
                    nombre=nombre,
                    apellido=apellido,
                    username=username,
                    contrasena=contrasena,
                    rol=rol,
                    grupo=grupo.id if grupo else None,
                    tutor=tutor.id if tutor else None
                )
                messages.success(request, "Usuario creado con éxito.")
                return redirect('crearUsuario')  # Redirige al mismo formulario para más usuarios
            except Grupo.DoesNotExist:
                messages.error(request, "El grupo seleccionado no existe.")
            except Tutor.DoesNotExist:
                messages.error(request, "El tutor seleccionado no existe.")
            except ValueError as ve:
                messages.error(request, f"Error: {ve}")
            except Exception as e:
                messages.error(request, f"Error inesperado: {e}")
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = CrearUsuarioForm()

    return render(request, "sistema/Vista_CrearUsuario.html", {'form': form})

def eliminarUsuario(request, usuarioId):
    
    alumnos = Alumno.objects.all()
    profesores = Profesor.objects.all()
    tutores = Tutor.objects.all()
    
    if (GestorDeUsuarios.eliminarUsuarioEscolar(usuarioId)):
        messages.success(request, "Usuario eliminado con éxito.")
        return redirect("listaUsuarios")
    else:
        messages.error(request, "Formulario inválido. Intenta de nuevo.")
        return render(request, "sistema/Vista_ListaUsuarios.html", {'alumnos': alumnos, 'profesores': profesores, 'tutores': tutores})


def modificarUsuario(request, usuarioId, rol):

    usuario = get_object_or_404(UsuarioEscolar, id=usuarioId)
    if request.method == "POST":
        actualizarUsuarioForm = ModificarUsuarioForm(request.POST, usuario=usuario)

        if actualizarUsuarioForm.is_valid():
            nombre = actualizarUsuarioForm.cleaned_data['nombre']
            apellido = actualizarUsuarioForm.cleaned_data['apellido']
            username = actualizarUsuarioForm.cleaned_data['username']
            contrasena = actualizarUsuarioForm.cleaned_data['contrasena']
            grupo = actualizarUsuarioForm.cleaned_data['grupo']
            tutor = actualizarUsuarioForm.cleaned_data['tutor']

            try:
                cambios = GestorDeUsuarios.modificarUsuarioEscolar(
                    usuarioId, 
                    nombre=nombre, 
                    apellido=apellido, 
                    username=username, 
                    contrasena=contrasena, 
                    rol=rol,
                    grupo=grupo.id if grupo else None,
                    tutor=tutor.id if tutor else None)
                if cambios:
                    messages.success(request, "Usuario actualizado con éxito.")
                else:
                    messages.info(request, "No se realizaron cambios.")
                return redirect('listaUsuarios')  # Cambiar a la vista o URL deseada
            except ValueError as e:
                actualizarUsuarioForm.add_error(None, str(e))
    else:
        actualizarUsuarioForm =  ModificarUsuarioForm(usuario=usuario)

    return render(request, 'sistema/Vista_ModificarUsuario.html', {'form': actualizarUsuarioForm, 'grupo': usuario})
    
    
def listarUsuarios(request):
    alumnos = Alumno.objects.all()
    profesores = Profesor.objects.all()
    tutores = Tutor.objects.all()
    return render(request, "sistema/Vista_ListaUsuarios.html", {'alumnos': alumnos, 'profesores': profesores, 'tutores': tutores})