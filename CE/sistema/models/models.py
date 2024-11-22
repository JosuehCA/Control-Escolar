from datetime import date
from abc import ABC, abstractmethod

from typing import List
from django.db import models as m
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from django.shortcuts import get_object_or_404

from datetime import date

from .models_actividades import Actividad



class MenuSemanal(m.Model):
    nombre = m.CharField(max_length=100)
    fecha_inicio = m.DateField()
    fecha_fin = m.DateField()
    platillos = m.ManyToManyField('Platillo', through='MenuPlatillo', related_name='menus')

    def __str__(self):
        return self.nombre

class MenuPlatillo(m.Model):
    menu = m.ForeignKey('MenuSemanal', on_delete=m.CASCADE, related_name='menu_platillos')
    platillo = m.ForeignKey('Platillo', on_delete=m.CASCADE, related_name='platillo_menus')
    dia = m.CharField(
        max_length=10,
        choices=[
            ('Lunes', 'Lunes'),
            ('Martes', 'Martes'),
            ('Miércoles', 'Miércoles'),
            ('Jueves', 'Jueves'),
            ('Viernes', 'Viernes'),
        ],
    )

    class Meta:
        unique_together = ('menu', 'platillo', 'dia')  # Evita duplicados en el mismo menú y día. Excepcion error platillo mismo dia

    def __str__(self):
        return f"{self.platillo.nombre} - {self.dia} ({self.menu.nombre})"


class Grupo(m.Model):
    """TDA Salón. Define aquellos grupos a los que pertenece un conjunto de estudiantes bajo la dirección 
    de un profesor."""

    nombre = m.CharField(max_length=2000)

    def __str__(self):
        return f'Grupo: {self.nombre}'
    
    def obtenerGrupoSegunNombre(nombreDeGrupo: str) -> 'Grupo':
        if(Grupo.objects.filter(nombre=nombreDeGrupo).exists()):
            return Grupo.objects.get(nombre=nombreDeGrupo)
        else:
            return None
    
    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"


class Platillo(m.Model):
    nombre = m.CharField(max_length=200)
    descripcion = m.TextField()
    consideraciones = m.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre



# Roles ---------------------------------------------------------------------------------------

class UsuarioEscolar(AbstractUser):
    """TDA Usuario Escolar. Define el rol común entre todos aquellos pertenecientes a la institución de una
    u otra manera (profesores, admnistrador, tutores, alumnos y nutricionista). Proporciona actividades 
    comunes dentro de estos roles."""

    def obtenerUsuarioSegunNombreDeUsuario(nombreDeUsuario: str ) -> 'UsuarioEscolar':
        if UsuarioEscolar.objects.filter(username=nombreDeUsuario).exists():
            return UsuarioEscolar.objects.get(username= nombreDeUsuario)
        else:
            return None
        
    def getNombreUsuario(self) -> str:
        return self.username

    def getNombre(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Usuario Escolar"
        verbose_name_plural = "Usuarios Escolares"

# Factories -----------------------------------------------------------------------------------
class CreadorDeUsuariosEscolares(ABC):
    @abstractmethod
    def crearUsuarioEscolar(self, **kwargs) -> UsuarioEscolar:    
        pass

class CreadorDeProfesores(CreadorDeUsuariosEscolares):

    def crearUsuarioEscolar(self, **kwargs) -> None:
        
        grupo_id = kwargs.get('grupo')
        
        try:
            grupo = Grupo.objects.get(id=grupo_id)
            return Profesor.objects.create(
                username=kwargs.get('username'),
                first_name=kwargs.get('nombre'),
                last_name=kwargs.get('apellido'),
                password=kwargs.get('contrasena'),
                grupo=grupo
            )
        except Grupo.DoesNotExist:
             print(f"Error: No se encontró el grupo con ID {grupo_id}")
            

class CreadorDeTutores(CreadorDeUsuariosEscolares):
    def crearUsuarioEscolar(self, **kwargs) -> None:
        return Tutor.objects.create(
            username=kwargs.get('username'),
            first_name=kwargs.get('nombre'),
            last_name=kwargs.get('apellido'),
            password=kwargs.get('contrasena')
        )

class CreadorDeAlumnos(CreadorDeUsuariosEscolares):
    
    def crearUsuarioEscolar(self, **kwargs) -> None:
        
        tutorId = kwargs.get('tutor')
        try:
            tutor = Tutor.objects.get(id=tutorId)
            return Alumno.objects.create(
                username=kwargs.get('username'),
                first_name=kwargs.get('nombre'),
                last_name=kwargs.get('apellido'),
                password=kwargs.get('contrasena'),
                tutorAlumno=tutor
            )
        except Tutor.DoesNotExist:
            print(f"Error: No se encontró el tutor con ID {tutorId}")
        
class CreadorDeNutricionistas(CreadorDeUsuariosEscolares):
    def crearUsuarioEscolar(self, **kwargs) -> None:
        return Nutricionista.objects.create(
            username=kwargs.get('username'),
            first_name=kwargs.get('nombre'),
            last_name=kwargs.get('apellido'),
            password=kwargs.get('contrasena')
        )

Creadores = {
    'Profesor': CreadorDeProfesores(),
    'Tutor': CreadorDeTutores(),
    'Alumno': CreadorDeAlumnos(),
    'Nutricionista': CreadorDeNutricionistas(),
}

class GestorDeGrupos(UsuarioEscolar):
    
    
    #Recibe el nombre y lista de alumnos a asignar al grupo
    @classmethod
    def crearGrupo(cls, nombre: str, alumnos: List['Alumno']) -> bool:
        if Grupo.objects.filter(nombre=nombre).exists():
            return False
        
        # Filtrar alumnos sin grupo
        alumnosSinGrupo = cls.obtenerAlumnosSinGrupo(alumnos)
        if not alumnosSinGrupo:
            return False

        # Crear el nuevo grupo y asignarlo a los alumnos
        nuevo_grupo = Grupo(nombre=nombre)
        nuevo_grupo.save()
        for alumno in alumnosSinGrupo:
            alumno.grupo = nuevo_grupo
            alumno.save()

        return True
      
    @classmethod
    def obtenerAlumnosSinGrupo(cls, alumnos: List['Alumno']) -> List['Alumno']:
        return [alumno for alumno in alumnos if alumno.grupo is None]

    @classmethod
    def eliminarGrupo(cls, grupoId) -> bool:
        try:
            grupo = Grupo.objects.get(id=grupoId)
            # Desasociar a los alumnos del grupo
            grupo.alumnos.update(grupo=None)
            grupo.delete()
            return True
        except Exception as e:
            print(f"Error al eliminar grupo: {e}")
            return False

    @classmethod
    def modificarGrupo(cls, grupo_id: int, nombre: str, alumnos: List['Alumno']) -> bool:
        try:
            grupo = Grupo.objects.get(id=grupo_id)
            grupo.nombre = nombre
            grupo.save()

            # Desasociar a los alumnos actuales del grupo
            grupo.alumnos.update(grupo=None)

            # Asignar los nuevos alumnos al grupo
            for alumno in alumnos:
                alumno.grupo = grupo
                alumno.save()

            return True
        except Grupo.DoesNotExist:
            print("El grupo no existe.")
            return False

    class Meta:
        verbose_name = "AdministradorGrupos"
        verbose_name_plural = "AdministradoresGrupos"
    

class GestorDeUsuarios(UsuarioEscolar):
    """TDA Administrador. Rol especial dentro del plantel cuyos permisos permiten controlar todo cuanto
    sea necesario. Tiene acceso a todos los apartados."""    


    @classmethod
    def crearUsuarioEscolar(cls, nombre, apellido, username, contrasena, rol, **kwargs) -> None:
        #Si el usuario ya existe, no se crea
        if UsuarioEscolar.objects.filter(username=username).exists():
            raise ValueError("Error: El usuario ya existe.")

        #Si el rol no es soportado, no se crea
        creador = Creadores.get(rol)
        if not creador:
            raise ValueError(f"Error: Rol no soportado: {rol}")

        try:
            creador.crearUsuarioEscolar(
                nombre=nombre,
                apellido=apellido,
                username=username,
                contrasena=contrasena,
                **kwargs
            )
        except ValueError as e:
            print(e)
        
    @classmethod
    def eliminarUsuarioEscolar(cls, usuarioId : int) -> bool:
        try:
            usuario = UsuarioEscolar.objects.get(id=usuarioId)
            usuario.delete()
            return True
        except Exception as e:
            print(f"Error al eliminar usuarios: {e}")
            return False
            
    @classmethod
    def modificarUsuarioEscolar(cls, usuarioId: int, nombre, apellido, nombreUsuario, contrasena, rol, **kwargs) -> bool:
        
        try:
            usuario = UsuarioEscolar.objects.get(id=usuarioId)
            if rol == 'Profesor':
                return cls.__modificarProfesor(usuario, nombre, apellido, nombreUsuario, contrasena, **kwargs)
            elif rol == 'Alumno':
                return cls.__modificarAlumno(usuario, nombre, apellido, nombreUsuario, contrasena, **kwargs)
            else:
                cls.__actualizarAtributos(usuario, nombre, apellido, nombreUsuario, contrasena)
                usuario.save()
                return True
                
        except UsuarioEscolar.DoesNotExist:
            print("El usuario no existe.")
            return False
    
    @staticmethod
    def __modificarProfesor(profesor, nombre, apellido, nombreUsuario, contrasena, **kwargs) -> bool:
        grupo_id = kwargs.get('grupo')
        try:
            GestorDeUsuarios.__actualizarAtributos(profesor, nombre, apellido, nombreUsuario, contrasena, grupo=grupo_id)
            profesor.save()
            return True
        except Grupo.DoesNotExist:
            print(f"Error: No se encontró el grupo con ID {grupo_id}")
            return False

    @staticmethod
    def __modificarAlumno(alumno, nombre, apellido, nombreUsuario, contrasena, **kwargs) -> bool:
        tutor_id = kwargs.get('tutor')
        try:
            GestorDeUsuarios.__actualizarAtributos(alumno, nombre, apellido, nombreUsuario, contrasena, tutor=tutor_id)
            alumno.save()
            return True
        except Tutor.DoesNotExist:
            print(f"Error: No se encontró el tutor con ID {tutor_id}")
            return False
    
    
    @staticmethod
    def __actualizarAtributos(usuario, nombre, apellido, nombreUsuario, contrasena, **kwargs) -> None:

        tutorId = kwargs.get('tutor')
        grupoId = kwargs.get('grupo')
        
        if nombre is not None:
            usuario.first_name = nombre
        if apellido is not None:
            usuario.last_name = apellido
        if nombreUsuario is not None:
            usuario.username = nombreUsuario
        if contrasena is not None:
            usuario.password = contrasena
        
        if hasattr(usuario, 'tutorAlumno') and tutorId is not None:
            try:
                tutor = Tutor.objects.get(id=tutorId)
                usuario.tutorAlumno = tutor
            except Tutor.DoesNotExist:
                print(f"Error: No se encontró el tutor con ID {tutorId}")

        if hasattr(usuario, 'grupo') and grupoId is not None:
            try:
                grupo = Grupo.objects.get(id=grupoId)
                usuario.grupo = grupo
            except Grupo.DoesNotExist:
                print(f"Error: No se encontró el grupo con ID {grupoId}")
            
            
    class Meta:
        verbose_name = "AdministradorUsuarios"
        verbose_name_plural = "AdministradoresUsuarios"


class Profesor(UsuarioEscolar):
    """TDA Profesor. Encargado de un subconjunto de grupos en específico y bajo mandato de un cierto grupo
    de alumnos. Contiene comportamientos respecto a estos alumnos, como asignación de actividades o pasar
    lista, y mantiene contacto directo con los tutores."""

    grupo = m.ForeignKey(Grupo, on_delete=m.RESTRICT, related_name="grupoProfesor")

    def asignarActividad(self, actividad: 'Actividad', grupo: Grupo) -> None:
        """Asigna una actividad a un grupo y actualiza la actividad actual de cada alumno del grupo."""
        actividad.grupo = grupo
        actividad.save()

        for alumno in grupo.alumnos.all():
            alumno.actividadActual = actividad
            alumno.save()

    def pasarLista(self, listaAsistencias: dict[int, bool]) -> None:
        for alumnoId, asistencia in listaAsistencias.items():
            alumno = Alumno.objects.get(id=alumnoId)
            RegistroAsistencia.objects.update_or_create(
                alumno=alumno,
                fecha=date.today(),
                defaults={'asistencia': asistencia}
            )            

    def asignarCalificacion(self, alumno: 'Alumno', grupo: 'Grupo', calificacion: int, comentario: str = "") -> None:
        """Asigna una calificación al comportamiento del día de un alumno"""

        if calificacion < 1 or calificacion > 5:
            raise ValueError("Error. Introduzca un valor dentro del rango (1-5)")
        
        # Crear o actualizar el registro de calificación para el alumno
        RegistroCalificaciones.objects.update_or_create(
            alumno=alumno,
            grupo=grupo,
            fecha=date.today(),
            defaults={
                'calificacion': calificacion,
                'comentario': comentario,
            }
        )
        
    class Meta:
            verbose_name = "Profesor"
            verbose_name_plural = "Profesores"

class RegistroCalificaciones(m.Model):
    alumno = m.ForeignKey('Alumno', on_delete=m.CASCADE, related_name='calificaciones')
    grupo = m.ForeignKey(Grupo, on_delete=m.CASCADE, related_name='calificacionesGrupo')
    calificacion = m.IntegerField(choices=[(i, i) for i in range(1, 6)])
    fecha = m.DateField(default=date.today)
    comentario = m.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('alumno', 'fecha')

    def __str__(self):
        return f"Calificación de {self.alumno.first_name} {self.alumno.last_name} en {self.grupo.nombre} el {self.fecha}"
    
    
class Tutor(UsuarioEscolar):
    """TDA Tutor. Tutor legal del alumno inscrito. Cuenta con acceso al sistema y puede visualizar toda la 
    información pertinente a sus tutorados."""

    def solicitarAltaTutorado(self, alumno: 'Alumno') -> None:
        if alumno.tutorAlumno:
            raise ValueError("El alumno ya tiene un tutor asignado")
        alumno.tutorAlumno = self
        alumno.save()

    def darDeBajaTutorado(self, alumno: 'Alumno') -> None:
        if alumno.tutorAlumno == self:
            alumno.tutorAlumno = None
            alumno.save()
        else:
            raise ValueError("El tutor no está asignado a este alumno")
        
    def agregarConsideracionMenu(self, alumno: 'Alumno', consideracion: dict) -> None:
        alumno.consideracionesMenu.append(consideracion)
        alumno.save()

    def verActividadActualTutorado(self, alumno: 'Alumno') -> Actividad:
        return alumno.actividadActual
    
    def generarReporteTutorado(self, alumno: 'Alumno'):
        pass

    
    class Meta:
        verbose_name = "Tutor"
        verbose_name_plural = "Tutores"


class Alumno(UsuarioEscolar):
    """TDA Alumno. Registrado solo para fines logísticos. Representa a cada alumno inscrito en el sistema y
    contiene un registro de su información académica."""

    tutorAlumno = m.ForeignKey(Tutor, on_delete=m.RESTRICT, related_name="tutorAlumno")
    grupo = m.ForeignKey(Grupo, on_delete=m.SET_NULL, related_name="alumnos", null=True, blank=True)
    asistencias = m.IntegerField(default=0)
    faltas = m.IntegerField(default=0)
    actividadActual = m.ForeignKey(Actividad, on_delete=m.SET_NULL, related_name="actividadActual", null=True, blank=True)
    consideracionesMenu = m.JSONField(default=list, blank=True)

    def asistirAClase(self) -> None:
        RegistroAsistencia.objects.update_or_create(
            alumno=self,
            fecha=date.today(),
            defaults={'asistencias': True, 'faltas':False}
        )
        self.asistencias += 1
        self.save()

    def faltarAClase(self) -> None:
        RegistroAsistencia.objects.update_or_create(
            alumno=self,
            fecha=date.today(),
            defaults={'asistencias': False, 'faltas':True}
        )
        self.faltas += 1
        self.save()

    def cambiarDeActividad(self, nuevaActividad: Actividad) -> None:
        self.actividadActual = nuevaActividad
        self.save()

    def getTutor(self) -> Tutor:
        return self.tutorAlumno

    def getAsistencias(self) -> int:
        return self.asistencias
    
    def getActividadActual(self) -> Actividad:
        return self.actividadActual

    def getFaltas(self) -> int:
        return self.faltas
    
    def getConsideracionesMenu(self) -> m.JSONField:
        return self.consideracionesMenu

    def __str__(self):
        return f"{self.getNombreUsuario()}: {self.getNombre()}"
    
class RegistroAsistencia(m.Model):
    alumno = m.ForeignKey(Alumno, on_delete=m.CASCADE, related_name="registrosAsistencia")
    fecha = m.DateField(auto_now_add=True)
    asistencias = m.BooleanField(default=False)
    faltas = m.BooleanField(default=False)

    class Meta:
        unique_together = ('alumno', 'fecha')  # Evita registros duplicados por día


class Nutricionista(UsuarioEscolar):
    """TDA Nutricionista. Responsable de la administración correcta de las comidas y ajustes al menú."""

    @staticmethod
    def crearRecomendaciones(nombre: str, descripcion: str, consideraciones: str)->Platillo:
        Platillo.objects.create(
            nombre=nombre, 
            descripcion=descripcion, 
            consideraciones=consideraciones) 

    @staticmethod 
    def modificarRecomendaciones(platillo_id: int, nombre: str, descripcion: str, consideraciones: str) -> None:
        """Método para editar los detalles de una recomendación en un menú"""
        try:
            platillo = Platillo.objects.get(id=platillo_id)
            platillo.nombre = nombre
            platillo.descripcion = descripcion
            platillo.consideraciones = consideraciones
            platillo.save()
        except Platillo.DoesNotExist:
            raise ValueError(f"No se encontró el platillo con ID {platillo_id}.")

    @staticmethod
    def eliminarRecomendaciones(platillo_id: int) -> None:
        """Elimina un platillo por su ID."""
        try:
            platillo = Platillo.objects.get(id=platillo_id)
            platillo.delete()
        except Platillo.DoesNotExist:
            raise ValueError("El platillo no existe y no puede ser eliminado.")

    class Meta:
        verbose_name = "Nutricionista"
        verbose_name_plural = "Nutricionistas"


class Chef(UsuarioEscolar):
    
    @staticmethod
    def crearMenuSemanal(nombre: str, fecha_inicio: date, fecha_fin:date)->MenuSemanal: 
        MenuSemanal.objects.create(
            nombre=nombre, 
            fecha_inicio=fecha_inicio, 
            fecha_fin=fecha_fin
        )

    @staticmethod
    def eliminarMenuSemanal(menu_id: int) -> None:
        """Elimina un menú semanal dado su ID."""
        try:
            menu = MenuSemanal.objects.get(id=menu_id)
            menu.delete()
        except MenuSemanal.DoesNotExist:
            raise ValueError(f"No se puede eliminar el menú con ID {menu_id}, ya que no existe.")

    @staticmethod
    def agregarPlatilloAlMenu(menu: MenuSemanal, platillo_id: int, dia: str) -> None:
        """Agrega un platillo al menú en un día específico."""
        try:
            platillo = Platillo.objects.get(id=platillo_id)
            MenuPlatillo.objects.create(menu=menu, platillo=platillo, dia=dia)
        except Platillo.DoesNotExist:
            raise ValueError(f"No se encontró el platillo con ID {platillo_id}.")

    @staticmethod
    def eliminarPlatilloDelMenu(menu: MenuSemanal, platillo_id: int, dia: str) -> None:
        """Elimina un platillo del menú en un día específico."""
        try:
            relacionMenuPlatillo = MenuPlatillo.objects.get(menu=menu, platillo_id=platillo_id, dia=dia)
            relacionMenuPlatillo.delete()
        except MenuPlatillo.DoesNotExist:
            raise ValueError(f"No existe una relación entre el platillo con ID {platillo_id} y el menú para el día {dia}.")

    def __str__(self):
        return f"Chef {self.nombre_completo}"
    