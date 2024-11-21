from django import forms

from sistema.models.models import Alumno, Grupo
from .models import *
from django.core.exceptions import ValidationError  

        
class CrearGrupoForm(forms.ModelForm):
    
    alumnos = forms.ModelMultipleChoiceField(
        queryset=Alumno.objects.all(),  # Obtiene todos los alumnos de la base de datos
        widget=forms.CheckboxSelectMultiple,  # Usa checkboxes para la selección múltiple
        required=True,  # Obliga a seleccionar al menos un alumno
        label="Selecciona los alumnos para el grupo"
    )

    class Meta:
        model = Grupo
        fields = ['nombre']  # Incluye 'alumnos' aquí para manejarlo en el formulario
        labels = {
            'nombre': 'Nombre del nuevo Grupo',
        }

class EliminarGrupoForm(forms.Form):
    grupos = forms.ModelMultipleChoiceField(
        queryset=Grupo.objects.all(),  
        widget=forms.CheckboxSelectMultiple,  # Usa checkboxes para selección múltiple
        required=True,  # Obliga a seleccionar al menos un grupo
        label="Selecciona Grupos para eliminar"
    )

class ActualizarGrupoForm(forms.ModelForm):
    
    alumnos = forms.ModelMultipleChoiceField(
        queryset=Alumno.objects.all(),  # Obtiene todos los alumnos de la base de datos
        widget=forms.CheckboxSelectMultiple,  # Usa checkboxes para la selección múltiple
        required=True,  # Obliga a seleccionar al menos un alumno
        label="Selecciona los alumnos para el grupo"
    )
    
    class Meta:
        model = Grupo
        fields = ['nombre']  # Campos editables
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre del grupo'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].required = False  # El campo 'nombre' no será obligatorio
    
