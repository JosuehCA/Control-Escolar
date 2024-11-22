from abc import ABC, abstractmethod
from typing import List
from django.db import models as m
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from datetime import date


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
    #alumnos = m.ManyToManyField('Alumno', related_name="alumnosGrupo")

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

    @classmethod
    def eliminarGruposAlumnosSeleccionados(cls, alumnos: List['Alumno']) -> None:
        for alumno in alumnos:
            alumno.grupo = None
            alumno.save()

    
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
                    GestorDeUsuarios._actualizarAtributos(profesor, nombre, apellido, username, contrasena)
                    profesor.save()
                    return True
                except Grupo.DoesNotExist:
                    print(f"Error: No se encontró el grupo con ID {grupo_id}")  
                    return False
            elif rol == 'Alumno':
                tutorId = kwargs.get('tutor')
                try:
                    alumno = Alumno.objects.get(id=usuarioId)
                    GestorDeUsuarios._actualizarAtributos(alumno, nombre, apellido, username, contrasena)
                    alumno.save() 
                    return True
                except Grupo.DoesNotExist:
                    print(f"Error: No se encontró el tutor con ID {tutorId}")
                    return False
            else:
                usuario = UsuarioEscolar.objects.get(id=usuarioId)
                GestorDeUsuarios._actualizarAtributos(usuario, nombre, apellido, username, contrasena)
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

    #listo
    def asignarActividad(self, actividad: 'Actividad', grupo: Grupo) -> None:
        """Asigna una actividad a un grupo y actualiza la actividad actual de cada alumno del grupo."""
        actividad.grupo = grupo
        actividad.save()

        for alumno in grupo.alumnos.all():
            alumno.actividadActual = actividad
            alumno.save()

    #listo
    def pasarLista(self, asistencias: dict[int, bool]) -> None:
        for alumno_id, asistencia in asistencias.items():
            alumno = Alumno.objects.get(id=alumno_id)
            RegistroAsistencia.objects.update_or_create(
                alumno=alumno,
                fecha=date.today(),
                defaults={'asistencia': asistencia}
            )            

    def asignarCalificacion(self, alumno: 'Alumno', grupo: 'Grupo', calif: int, comentario: str = "") -> None:
        """
        Asigna una calificación al comportamiento del día de un alumno
        y la guarda en el modelo RegistroCalificaciones.
        """
        if calif < 1 or calif > 5:
            raise ValueError("La calificación debe estar entre 1 y 5.")
        
        # Crear o actualizar el registro de calificación para el alumno
        registro, created = RegistroCalificaciones.objects.update_or_create(
            alumno=alumno,
            grupo=grupo,
            fecha=date.today(),
            defaults={
                'calificacion': calif,
                'comentario': comentario,
            }
        )
        if created:
            print(f"Nuevo registro de calificación creado para {alumno.first_name}")
        else:
            print(f"Registro de calificación actualizado para {alumno.first_name}")

    class Meta:
            verbose_name = "Profesor"
            verbose_name_plural = "Profesores"

class RegistroCalificaciones(m.Model):
    alumno = m.ForeignKey('Alumno', on_delete=m.CASCADE, related_name='calificaciones')
    grupo = m.ForeignKey(Grupo, on_delete=m.CASCADE, related_name='calificaciones_grupo')
    calificacion = m.IntegerField(choices=[(i, i) for i in range(1, 6)])
    fecha = m.DateField(default=date.today)
    comentario = m.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('alumno', 'fecha')

    def __str__(self):
        return f"Calificación de {self.alumno.getNombre()} en {self.grupo.nombre} el {self.fecha}"
    
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

    tutorAlumno = m.ForeignKey(Tutor, on_delete=m.RESTRICT, related_name="tutor_alumno")
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
    
    def getGrupo(self) -> Grupo:
        return self.grupo
    
    def setAsistencias(self, asistencias: int) -> None:
        self.asistencias = asistencias
    
    def setFaltas(self, faltas: int) -> None:
        self.faltas = faltas

    class Meta:
        verbose_name = "Alumno"
        verbose_name_plural = "Alumnos"

    def __str__(self):
        return f"{self.getNombreUsuario()}: {self.getNombre()}"
    
class RegistroAsistencia(m.Model):
    alumno = m.ForeignKey(Alumno, on_delete=m.CASCADE, related_name="registros_asistencia")
    fecha = m.DateField(auto_now_add=True)
    asistencias = m.BooleanField(default=False)
    faltas = m.BooleanField(default=False)

    class Meta:
        unique_together = ('alumno', 'fecha')  # Evita registros duplicados por día


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
