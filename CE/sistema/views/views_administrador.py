from pyexpat.errors import messages
from django.shortcuts import render
from django.shortcuts import redirect

from sistema.forms_usuarios import CrearUsuarioForm, EliminarUsuarioForm
from sistema.models.models import Alumno, Grupo, Administrador, Profesor, Tutor
from django.shortcuts import redirect
from sistema.forms_grupos import CrearGrupoForm, EliminarGrupoForm, ModificarGrupoForm

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
            
        if Administrador.crearGrupo(nombre, list(alumnos)):
            messages.success(request, "Grupo creado con éxito.")
            return redirect('crearGrupo')
        else:
            messages.error(request, "Error al crear el grupo.")
    else:
        form = CrearGrupoForm()

    return render(request, 'sistema/Vista_CrearGrupo.html', {
        'form': form
    })
    
def eliminarGrupo(request):
    
    if request.method == 'POST':
        form = EliminarGrupoForm(request.POST)
        if form.is_valid():
            grupos = form.cleaned_data['grupos']
            
        try:
            Administrador.eliminarGrupo(list(grupos))
            messages.success(request, "Grupos eliminados con éxito.")
        except:
            messages.error(request, "Error al eliminar grupos.")
        return redirect('eliminarGrupo')
    else:
        form = EliminarGrupoForm()  

    return render(request, "sistema/Vista_EliminarGrupo.html", {'form': form})
    
def modificarGrupo(request):
    if request.method == 'POST':
        form = ModificarGrupoForm(request.POST)
        if form.is_valid():
            grupo = form.cleaned_data['grupo']
            nuevo_nombre = form.cleaned_data['nombre']
            nuevos_alumnos = form.cleaned_data['alumnos']

            try:
                if nuevo_nombre:
                    grupo.nombre = nuevo_nombre
                
                if nuevos_alumnos:
                    Administrador.editarGrupo(grupo.id, grupo.nombre, list(nuevos_alumnos))

                messages.success(request, "Grupo modificado con éxito.")
                return redirect('modificarGrupo')
            except Exception as e:
                messages.error(request, f"Error al modificar el grupo: {str(e)}")
    else:
        form = ModificarGrupoForm()

    return render(request, 'sistema/Vista_ModificarGrupo.html', {'form': form})

    
def listar_grupos(request):
    grupos = Grupo.objects.prefetch_related('alumnos').all()  # Prefetch para cargar alumnos de forma eficiente
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
                Administrador.crearUsuarioEscolar(
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
            except Exception as e:
                messages.error(request, f"Error al crear usuario: {e}")
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = CrearUsuarioForm()

    return render(request, "sistema/Vista_CrearUsuario.html", {'form': form})

def eliminarUsuario(request):
    if request.method == 'POST':
        form = EliminarUsuarioForm(request.POST)
        if form.is_valid():
            usuarios = form.cleaned_data['usuarios']  # Lista de objetos UsuarioEscolar
            try:
                # Pasar solo los IDs de los usuarios al método
                Administrador.eliminarUsuarioEscolar([usuario.id for usuario in usuarios])
                messages.success(request, "Usuarios eliminados con éxito.")
            except Exception as e:
                messages.error(request, f"Error al eliminar: {str(e)}")
        else:
            messages.error(request, "Formulario inválido. Intenta de nuevo.")
        return redirect('eliminarUsuario')
    else:
        form = EliminarUsuarioForm()
    
    return render(request, "sistema/Vista_EliminarUsuario.html", {'form': form})


def modificarUsuario(request):
    return render(request, "sistema/Vista_ModificarUsuario.html")

def listarUsuarios(request):
    alumnos = Alumno.objects.all()
    profesores = Profesor.objects.all()
    tutores = Tutor.objects.all()
    return render(request, "sistema/Vista_ListaUsuarios.html", {'alumnos': alumnos, 'profesores': profesores, 'tutores': tutores})