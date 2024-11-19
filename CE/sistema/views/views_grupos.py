from django.shortcuts import render
from django.shortcuts import redirect

from sistema.models.models import Alumno, Grupo, Administrador

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