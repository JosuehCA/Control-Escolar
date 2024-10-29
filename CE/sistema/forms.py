from django import forms
from .models import *

class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['nombre', 'horaInicio', 'horaFinal', 'horario']

        labels = {
            'nombre': 'Nombre de la Actividad',
            'horaInicio': 'Hora de Inicio',
            'horaFinal': 'Hora de Finalización',
            'horario': 'Horario Asociado', 
        }

        widgets = {
            'horaInicio': forms.TimeInput(attrs={'type': 'time'}),
            'horaFinal': forms.TimeInput(attrs={'type': 'time'}),
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

class CrearHorarioForm(forms.ModelForm):
    class Meta:
        model = HorarioDeActividades
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