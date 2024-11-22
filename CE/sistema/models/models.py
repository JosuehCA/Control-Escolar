from abc import ABC, abstractmethod
from typing import List
from django.db import models as m
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from .models_actividades import Actividad


class MenuSemanal(m.Model):
    """TDA Menu. Define un Menú de comidas personalizable de acuerdo al administrador, y tomando en cuenta
    ciertas indicaciones que los tutores manifiesten."""

    nombre = m.CharField(max_length=100)
    fecha_inicio = m.DateField()
    fecha_fin = m.DateField()

    def __str__(self):
        return self.nombre

class Grupo(m.Model):
    """TDA Salón. Define aquellos grupos a los que pertenece un conjunto de estudiantes bajo la dirección 
    de un profesor."""

    nombre = m.CharField(max_length=2000)
    alumnos = m.ManyToManyField('Alumno', related_name="alumnosGrupo")

    def __str__(self):
        return f'Grupo: {self.nombre}'
    
    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"


class Platillo(m.Model):
    DIAS_SEMANA = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
    ]
    
    nombre = m.CharField(max_length=200)
    descripcion = m.TextField()
    consideraciones = m.TextField(blank=True, null=True)
    dia = m.CharField(
        max_length=10,
        choices=DIAS_SEMANA,
        blank=True,  
        null=True,
        help_text="Día de la semana al que pertenece este platillo."
    )
    menu = m.ForeignKey(
        'MenuSemanal',
        on_delete=m.CASCADE,
        related_name='platillos',
        null=True,
        blank=True,
        help_text="Menú al que pertenece este platillo."
    )

    def __str__(self):
        return f"{self.nombre} ({self.dia or 'Sin Día'})"



# Roles ---------------------------------------------------------------------------------------


class UsuarioEscolar(AbstractUser):
    """TDA Usuario Escolar. Define el rol común entre todos aquellos pertenecientes a la institución de una
    u otra manera (profesores, admnistrador, tutores, alumnos y nutricionista). Proporciona actividades 
    comunes dentro de estos roles."""

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

FACTORIES = {
    'Profesor': CreadorDeProfesores(),
    'Tutor': CreadorDeTutores(),
    'Alumno': CreadorDeAlumnos(),
    'Nutricionista': CreadorDeNutricionistas(),
}

class GestorDeGrupos(UsuarioEscolar):
    
    @classmethod
    def crearGrupo(cls, nombre: str, alumnos: List['Alumno']) -> bool:
        
        if Grupo.objects.filter(nombre=nombre).exists():
            return False
        
        alumnosSinGrupo = cls.obtenerAlumnosSinGrupo(alumnos)
        if not alumnosSinGrupo:
            return False
        
        nuevo_grupo = Grupo(nombre=nombre)
        nuevo_grupo.save()  # Guardamos primero para poder asignar M2M
        nuevo_grupo.alumnos.set(alumnosSinGrupo)  # Añadimos los alumnos seleccionados al grupo
        nuevo_grupo.save()
        return True
      
    @classmethod      
    def obtenerAlumnosSinGrupo(cls, alumnos: List['Alumno']) -> List['Alumno']:
        alumnosSinGrupo = [] 
        for alumno in alumnos:
            if not Grupo.objects.filter(alumnos=alumno).exists():
                alumnosSinGrupo.append(alumno)  
        return alumnosSinGrupo

    @classmethod
    def eliminarGrupo(cls, grupoId) -> bool:
        try:
            grupo = Grupo.objects.get(id=grupoId)
            grupo.delete()
            return True
        except Exception as e:
            print(f"Error al eliminar grupo: {e}")
            return False

    @classmethod
    def modificarGrupo(cls, grupo_id: int, nombre: str, alumnos: List['Alumno']) -> bool:
        try:
            cls.eliminarGruposAlumnosSeleccionados(alumnos)
            grupo = Grupo.objects.get(id=grupo_id)
            grupo.nombre = nombre
            grupo.alumnos.set(alumnos)
            grupo.save()
            return True
        except Grupo.DoesNotExist:
            print("El grupo no existe.")
            return False

    @classmethod
    def eliminarGruposAlumnosSeleccionados(cls, alumnos: List['Alumno']) -> None:
        for alumno in alumnos:
            Grupo.objects.filter(alumnos=alumno).update(alumnos=None)
    
    class Meta:
        verbose_name = "AdministradorGrupos"
        verbose_name_plural = "AdministradoresGrupos"
    

class GestorDeUsuarios(UsuarioEscolar):
    """TDA Administrador. Rol especial dentro del plantel cuyos permisos permiten controlar todo cuanto
    sea necesario. Tiene acceso a todos los apartados."""    

    @classmethod
    def crearUsuarioEscolar(cls, nombre, apellido, username, contrasena, rol, **kwargs) -> None:
        if UsuarioEscolar.objects.filter(username=username).exists():
            raise ValueError("Error: El usuario ya existe.")

        factory = FACTORIES.get(rol)
        if not factory:
            raise ValueError(f"Error: Rol no soportado: {rol}")

        try:
            factory.crearUsuarioEscolar(
                nombre=nombre,
                apellido=apellido,
                username=username,
                contrasena=contrasena,
                **kwargs
            )
        except ValueError as e:
            print(e)
        
    @classmethod
    def eliminarUsuarioEscolar(cls, usuarioId : int) -> None:
        try:
            usuario = UsuarioEscolar.objects.get(id=usuarioId)
            usuario.delete()
        except Exception as e:
            print(f"Error al eliminar usuarios: {e}")
            
    @classmethod
    def modificarUsuarioEscolar(cls, usuarioId: int, nombre, apellido, username, contrasena, rol, **kwargs) -> bool:
        
        try:
            if rol == 'Profesor':
                grupo_id = kwargs.get('grupo')
                try:
                    profesor = Profesor.objects.get(id=usuarioId)
                    GestorDeGrupos._actualizarAtributos(profesor, nombre, apellido, username, contrasena)
                    profesor.save()
                    return True
                except Grupo.DoesNotExist:
                    print(f"Error: No se encontró el grupo con ID {grupo_id}")  
                    return False
            elif rol == 'Alumno':
                tutorId = kwargs.get('tutor')
                try:
                    alumno = Alumno.objects.get(id=usuarioId)
                    GestorDeGrupos._actualizarAtributos(alumno, nombre, apellido, username, contrasena)
                    alumno.save() 
                    return True
                except Grupo.DoesNotExist:
                    print(f"Error: No se encontró el tutor con ID {tutorId}")
                    return False
            else:
                usuario = UsuarioEscolar.objects.get(id=usuarioId)
                GestorDeGrupos._actualizarAtributos(usuario, nombre, apellido, username, contrasena)
                usuario.save()
                return True
                
        except UsuarioEscolar.DoesNotExist:
            print("El usuario no existe.")
            return False
    
    @staticmethod
    def _actualizarAtributos(usuario, nombre, apellido, username, contrasena, **kwargs):
        """
        Actualiza los atributos básicos del usuario si se proporcionan valores.
        """
        tutor_id = kwargs.get('tutor')
        grupo_id = kwargs.get('grupo')
        
        if nombre is not None:
            usuario.first_name = nombre
        if apellido is not None:
            usuario.last_name = apellido
        if username is not None:
            usuario.username = username
        if contrasena is not None:
            usuario.password = contrasena
        
        if hasattr(usuario, 'tutorAlumno') and tutor_id is not None:
            try:
                tutor = Tutor.objects.get(id=tutor_id)
                usuario.tutorAlumno = tutor
            except Tutor.DoesNotExist:
                print(f"Error: No se encontró el tutor con ID {tutor_id}")

        if hasattr(usuario, 'grupo') and grupo_id is not None:
            try:
                grupo = Grupo.objects.get(id=grupo_id)
                usuario.grupo = grupo
            except Grupo.DoesNotExist:
                print(f"Error: No se encontró el grupo con ID {grupo_id}")
            
    class Meta:
        verbose_name = "AdministradorUsuarios"
        verbose_name_plural = "AdministradoresUsuarios"


class Profesor(UsuarioEscolar):
    """TDA Profesor. Encargado de un subconjunto de grupos en específico y bajo mandato de un cierto grupo
    de alumnos. Contiene comportamientos respecto a estos alumnos, como asignación de actividades o pasar
    lista, y mantiene contacto directo con los tutores."""

    grupo = m.ForeignKey(Grupo, on_delete=m.RESTRICT, related_name="grupo_profesor")


    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"


class Alumno(UsuarioEscolar):
    """TDA Alumno. Registrado solo para fines logísticos. Representa a cada alumno inscrito en el sistema y
    contiene un registro de su información académica."""
    tutorAlumno = m.ForeignKey('Tutor', on_delete=m.RESTRICT, related_name="tutor_alumno")
    asistencias = m.IntegerField(default=0)
    faltas = m.IntegerField(default=0)
    actividadActual = m.ForeignKey(Actividad, on_delete=m.SET_NULL, related_name="actividadActual", null=True, blank=True)
    consideracionesMenu = m.JSONField(default=list, blank=True)


    def asistirAClase(self) -> None:
        self.asistencias += 1
        self.save()
    
    def faltarAClase(self) -> None:
        self.faltas += 1
        self.save()

    def cambiarDeActividad(self, nuevaActividad: Actividad) -> None:
        self.actividadActual = nuevaActividad
        self.save()

    def getTutor(self) -> "Tutor":
        return self.tutorAlumno

    def getAsistencias(self) -> int:
        return self.asistencias
    
    def getActividadActual(self) -> Actividad:
        return self.actividadActual

    def getFaltas(self) -> int:
        return self.faltas
    
    def getConsideracionesMenu(self) -> m.JSONField:
        return self.consideracionesMenu
    

    class Meta:
        verbose_name = "Alumno"
        verbose_name_plural = "Alumnos"

    def __str__(self):
        return f"{self.getNombreUsuario()}: {self.getNombre()}"
    
class Tutor(UsuarioEscolar):
    """TDA Tutor. Tutor legal del alumno inscrito. Cuenta con acceso al sistema y puede visualizar toda la 
    información pertinente a sus tutorados."""

    def solicitarAltaTutorado(self, alumno: Alumno) -> None:
        if alumno.tutorAlumno:
            raise ValueError("El alumno ya tiene un tutor asignado")
        alumno.tutorAlumno = self
        alumno.save()

    def darDeBajaTutorado(self, alumno: Alumno) -> None:
        if alumno.tutorAlumno == self:
            alumno.tutorAlumno = None
            alumno.save()
        else:
            raise ValueError("El tutor no está asignado a este alumno")
        
    def agregarConsideracionMenu(self, alumno: Alumno, consideracion: dict) -> None:
        alumno.consideracionesMenu.append(consideracion)
        alumno.save()

    def verActividadActualTutorado(self, alumno: Alumno) -> Actividad:
        return alumno.actividadActual
    
    def generarReporteTutorado(self, alumno: Alumno):
        pass

    
    class Meta:
        verbose_name = "Tutor"
        verbose_name_plural = "Tutores"


class Nutricionista(UsuarioEscolar):
    """TDA Nutricionista. Responsable de la administración correcta de las comidas y ajustes al menú."""

    def crearPlatillo(nombre: str, descripcion: str, consideraciones: str):
        Platillo.objects.create(
            nombre=nombre, 
            descripcion=descripcion, 
            consideraciones=consideraciones)
        
    

    class Meta:
        verbose_name = "Nutricionista"
        verbose_name_plural = "Nutricionistas"
