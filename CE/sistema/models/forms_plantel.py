from django import forms
from sistema.models.models_actividades import *
from django.core.exceptions import ValidationError  
from typing import Any, Dict
from datetime import date, time


class BaseActividadForm(forms.ModelForm):
    @staticmethod
    def validarDatosFormulario(formulario, horaInicio, horaFinal, actividad=None):
        if horaFinal and horaInicio:
            if horaFinal <= horaInicio:
                formulario.add_error('horaFinal', 'La hora de finalización debe ser mayor que la hora de inicio.')
                return

            gestorActividades=GestorActividades()
                # Determinar el horario
            if actividad:
                # Si es una actualización, usar el horario de la actividad
                horario = actividad.horario
            else:
                # Si es una creación, obtener el horario del formulario
                horario = formulario.cleaned_data.get('horario')

            # Validar que el horario exista
            if not horario:
                formulario.add_error("horario", "Debe seleccionar un horario válido.")
                return

            # Validar rango permitido
            if not gestorActividades.validarRangoDeActividad(horario, horaInicio, horaFinal):
                formulario.add_error("horaFinal", "La actividad está fuera del horario permitido.")
            


            if actividad:
                #horario = actividad.horario
                listaActividades = horario.actividades.exclude(id=actividad.id)
                for actividadExistente in listaActividades:
                    if actividadExistente.fecha == actividad.fecha:
                        if (horaInicio < actividadExistente.horaFinal and horaFinal > actividadExistente.horaInicio):
                            formulario.add_error("horaFinal", f"Conflicto de horario con la actividad '{actividadExistente.nombre}' que va de {actividadExistente.horaInicio} a {actividadExistente.horaFinal}.")
                            return


class CrearActividadForm(BaseActividadForm):
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
            'grupo': forms.Select()
        }

    def clean(self):
        datosValidados = super().clean()
        horaInicio = datosValidados.get('horaInicio')
        horaFinal = datosValidados.get('horaFinal')
        self.validarDatosFormulario(self, horaInicio, horaFinal)
        return datosValidados


class ActualizarActividadForm(BaseActividadForm):
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
    def clean(self):
        datosValidados = super().clean()
        horaInicio = datosValidados.get('horaInicio')
        horaFinal = datosValidados.get('horaFinal')
        self.validarDatosFormulario(self, horaInicio, horaFinal, self.instance)
        return datosValidados



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
        
