from django.db import models as m
from django.utils import timezone

class HorarioEscolar(m.Model):
    fecha = m.DateField(null=True, blank=True, unique=True)  # Opcional para el horario predeterminado
    horaEntrada = m.TimeField()
    horaSalida = m.TimeField()

    def __str__(self) -> str:
        if self.fecha:
            return f"Horario: {self.fecha} ({self.horaEntrada} - {self.horaSalida})"
        return f"Horario Predeterminado ({self.horaEntrada} - {self.horaSalida})"

    class Meta:
        verbose_name_plural = "Horarios"

class GestorHorarios():

    @classmethod
    def obtenerHorarioPorDefecto(cls) -> int:
        """Obtiene el ID de un horario predeterminado."""
        horarioPorDefecto, creado = HorarioEscolar.objects.get_or_create(
            fecha=None, 
            defaults={'horaEntrada': '06:00', 'horaSalida': '12:00'}
        )
        return horarioPorDefecto.id  

    @staticmethod
    def crearHorarioEscolar(fecha: m.DateField, horaEntrada: m.TimeField, horaSalida: m.TimeField) -> HorarioEscolar:
        """Crea un horario nuevo."""
        return HorarioEscolar.objects.create(fecha=fecha, horaEntrada=horaEntrada, horaSalida=horaSalida)

    @staticmethod
    def eliminarHorarioEscolar(horarioId: int) -> bool:
        """Elimina un horario específico por su ID."""
        try:
            horario = HorarioEscolar.objects.get(id=horarioId)
            horario.delete()
            return True
        except HorarioEscolar.DoesNotExist:
            return False

class Actividad(m.Model):
    nombre = m.CharField(max_length=200, default="Actividad sin Nombre")
    descripcion = m.CharField(max_length=500, default="Actividad sin descripción")
    horaInicio = m.TimeField()
    horaFinal = m.TimeField()
    fecha = m.DateField(default=timezone.localdate)
    horario = m.ForeignKey(HorarioEscolar, related_name='actividades', on_delete=m.CASCADE, default=GestorHorarios.obtenerHorarioPorDefecto)
    grupo = m.ForeignKey('Grupo', on_delete=m.CASCADE, related_name='actividades', null=True, blank=True)

class GestorActividades():

    # models_actividades.py
    def obtener_grupo():
        from .models import Grupo
        return Grupo

    
    def agregarActividad(self, horario: HorarioEscolar, nombre: str, descripcion: str, horaInicio: m.TimeField, horaFinal: m.TimeField, fecha: m.DateField, grupo: obtener_grupo) -> Actividad:
        """Agrega una actividad a un horario, validando rango y conflictos."""
    
        return Actividad.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            horaInicio=horaInicio,
            horaFinal=horaFinal,
            horario=horario,
            fecha=fecha,
            grupo=grupo
        )

    def eliminarActividad(self, actividadId: int) -> bool:
        """Elimina una actividad específica por su ID."""
        try:
            actividad = Actividad.objects.get(id=actividadId)
            actividad.delete()
            return True
        except Actividad.DoesNotExist:
            return False
        
    def actualizarActividad(
        self,
        actividad: Actividad,
        nuevoNombre: str,
        nuevaDescripcion: str,
        nuevaHoraInicio: m.TimeField,
        nuevaHoraFinal: m.TimeField
    ) -> bool:
        """Actualiza los datos de la actividad directamente en la base de datos."""
        # Asignar los nuevos valores directamente
        actividad.nombre = nuevoNombre
        actividad.descripcion = nuevaDescripcion
        actividad.horaInicio = nuevaHoraInicio
        actividad.horaFinal = nuevaHoraFinal

        # Guardar los cambios en la base de datos
        actividad.save()
        return True

    def filtrarActividadesPorFecha(self, fecha: m.DateField) -> m.QuerySet:
        """Devuelve las actividades para una fecha específica."""
        return Actividad.objects.filter(fecha=fecha)
    
    def validarRangoDeActividad(self, horario: HorarioEscolar, horaInicio: m.TimeField, horaFinal: m.TimeField) -> bool:
        """Valida si un rango horario está dentro del horario definido."""
        if horario.horaEntrada <= horaInicio and horaFinal <= horario.horaSalida:
            return True
        return False
    
    def verificarSolapamientos(
        self,
        horario: HorarioEscolar,
        horaInicio: m.TimeField,
        horaFinal: m.TimeField,
        fecha: m.DateField 
    ) -> Actividad:
        """Verifica si una nueva actividad solapa con alguna existente en el horario."""
        listaActividades = Actividad.objects.filter(
            horario=horario,
            fecha=fecha
        )
        for actividad in listaActividades:
            if (
                (horaInicio < actividad.horaFinal and horaFinal > actividad.horaInicio) or 
                (actividad.horaInicio < horaFinal and actividad.horaFinal > horaInicio)
            ):
                return actividad
        return None
