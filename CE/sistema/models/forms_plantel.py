from django import forms
from sistema.models.models_actividades import *
from django.core.exceptions import ValidationError  
from typing import Any, Dict
from datetime import date, time


class CrearActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['nombre', 'descripcion', 'horaInicio', 'horaFinal', 'horario', 'fecha', 'grupo']  

        labels = {
            'nombre': 'Nombre de la Actividad',
            'descripcion': 'Descripción',
            'horaInicio': 'Hora de Inicio',
            'horaFinal': 'Hora de Finalización',
            'horario': 'Horario Asociado',
            'fecha': 'Fecha de la Actividad',  
            'grupo': 'Grupo Asociado',  

        }

        widgets = {
            'horaInicio': forms.TimeInput(attrs={'type': 'time'}),
            'horaFinal': forms.TimeInput(attrs={'type': 'time'}),
            'horario': forms.Select(),
            'fecha': forms.DateInput(attrs={'type': 'date', 'value': timezone.localdate()}),
            'grupo': forms.Select()  # Usar Select widget para 'grupo'
        }


class ActualizarActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['nombre', 'descripcion', 'horaInicio', 'horaFinal']

        labels = {
            'nombre': 'Nombre de la Actividad',
            'descripcion': 'Descripción',
            'horaInicio': 'Hora de Inicio',
            'horaFinal': 'Hora de Finalización',
        }

        widgets = {
            'horaInicio': forms.TimeInput(attrs={'type': 'time'}),
            'horaFinal': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self) -> Dict[str, Any]:
        datosValidados = super().clean()
        horaInicio = datosValidados.get('horaInicio')
        horaFinal = datosValidados.get('horaFinal')
        self.validarActualizacion(horaInicio, horaFinal, datosValidados)
        return datosValidados


    def validarActualizacion(self, horaInicio: time, horaFinal: time, datosValidados: Dict[str, Any]) -> None:
        # Validación de horas
        if horaFinal and horaInicio:
            if horaFinal <= horaInicio:
                self.add_error('horaFinal', 'La hora de finalización debe ser mayor que la hora de inicio.')
                return

            # Validación de rango horario
            gestorActividades = GestorActividades()
            if not gestorActividades.validarRangoDeActividad(self.instance.horario, horaInicio, horaFinal):
                self.add_error("horaFinal", "La actividad está fuera del horario permitido.")
                return

            # Verificación de conflictos de horario con otras actividades
            horario = self.instance.horario
            #listaActividades = horario.actividades.exclude(id=self.instance.id if self.instance.id else None)
            listaActividades = horario.actividades.exclude(id=self.instance.id)
            
            for actividad in listaActividades:
                # Verificamos si las actividades ocurren en la misma fecha y si las horas se solapan
                if actividad.fecha == self.instance.fecha:
                    if (horaInicio < actividad.horaFinal and horaFinal > actividad.horaInicio):
                        self.add_error("horaFinal", f"Conflicto de horario con la actividad '{actividad.nombre}' que va de {actividad.horaInicio} a {actividad.horaFinal}.")
                        return 
        
        # Comparar si los datos actuales son iguales a los existentes en la instancia
        camposRevisar = ['nombre', 'descripcion', 'horaInicio', 'horaFinal']
        cambiosRealizados = any(
            datosValidados.get(campo) != getattr(self.instance, campo) for campo in camposRevisar
        )

        if not cambiosRealizados:
            self.add_error(None, "No se realizaron cambios en los datos de la actividad.")


class CrearHorarioForm(forms.ModelForm):
    class Meta:
        model = HorarioEscolar
        fields = ['fecha', 'horaEntrada', 'horaSalida']
        labels = {
            'fecha': 'Fecha',
            'horaEntrada': 'Hora de Entrada',
            'horaSalida': 'Hora de Salida',
        }
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'horaEntrada': forms.TimeInput(attrs={'type': 'time'}),
            'horaSalida': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_fecha(self)-> date:
        datosValidados = super().clean()
        fecha = datosValidados.get('fecha')
        self.comprobarExistenciaHorario(fecha)
        return fecha

    def comprobarExistenciaHorario(self, fecha: date) -> None:
        if HorarioEscolar.objects.filter(fecha=fecha).exists():
            raise ValidationError("Ya existe un horario para esta fecha. Por favor, elige otra fecha.")
        
