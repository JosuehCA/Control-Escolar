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

class GestorActividades():
    
    def agregarActividad(self, horario: HorarioEscolar, nombre: str, descripcion: str, horaInicio: m.TimeField, horaFinal: m.TimeField, fecha: m.DateField) -> Actividad:
        """Agrega una actividad a un horario, validando rango y conflictos."""

        # Validación: horaFinal debe ser mayor que horaInicio
        if horaFinal <= horaInicio:
            raise ValueError("La hora de finalización debe ser mayor que la hora de inicio.")
        
        if not self.validarRangoDeActividad(horario, horaInicio, horaFinal):
            raise ValueError("La actividad está fuera del horario permitido")
    
        actividadConflictiva = self.verificarSolapamientos(horario, horaInicio, horaFinal, fecha)
        if actividadConflictiva:
            raise ValueError(
                f"Conflicto con la actividad '{actividadConflictiva.nombre}' "
                f"(Inicio: {actividadConflictiva.horaInicio}, Fin: {actividadConflictiva.horaFinal})"
            )
    
        return Actividad.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            horaInicio=horaInicio,
            horaFinal=horaFinal,
            horario=horario,
            fecha=fecha  
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
        nombre: str,
        descripcion: str,
        horaInicio: m.TimeField,
        horaFinal: m.TimeField
    ) -> bool:
        """Actualiza el nombre, descripción y las horas de la actividad. No permite modificar la fecha ni el horario asociado"""
        # Verificación de cambios en las horas
        if actividad.horaInicio != horaInicio or actividad.horaFinal != horaFinal:
            # Validación: horaFinal debe ser mayor que horaInicio
            if horaFinal <= horaInicio:
                raise ValueError("La hora de finalización debe ser mayor que la hora de inicio.")
            
            # Verificar conflictos de horario, excluyendo la propia actividad
            listaActividades = actividad.horario.actividades.exclude(id=actividad.id)
            for otra_actividad in listaActividades:
                if (horaInicio < otra_actividad.horaFinal and horaFinal > otra_actividad.horaInicio):
                    raise ValueError("Conflicto de horario con otra actividad.")
            
            # Verificar si las horas están dentro del rango permitido por el horario
            if not self.validarRangoDeActividad(actividad.horario, horaInicio, horaFinal):
                raise ValueError("La actividad está fuera del horario permitido.")

            # Actualizar las horas si todo es válido
            actividad.horaInicio = horaInicio
            actividad.horaFinal = horaFinal

        # Verificación de cambios en el nombre y la descripción
        if actividad.nombre != nombre or actividad.descripcion != descripcion:
            actividad.nombre = nombre
            actividad.descripcion = descripcion

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