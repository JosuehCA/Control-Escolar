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

class ModificarGrupoForm(forms.Form):
    
    grupo = forms.ModelMultipleChoiceField(
        queryset=Grupo.objects.all(),  
        widget=forms.CheckboxSelectMultiple,  # Usa checkboxes para selección múltiple
        required=True,  # Obliga a seleccionar al menos un grupo
        label="Selecciona Grupos para modificar"
    )
     
    nombre = forms.CharField(
        max_length=2000,
        required=False,  # El nombre será opcional
        label="Nuevo nombre del grupo",
        widget=forms.TextInput(attrs={'placeholder': 'Deja vacío para mantener el nombre actual'})
    )

    alumnos = forms.ModelMultipleChoiceField(
        queryset=Alumno.objects.all(),  # Lista de alumnos
        widget=forms.CheckboxSelectMultiple,  # Selección múltiple con checkboxes
        required=False,  # Dejar vacío para mantener los alumnos actuales
        label="Selecciona alumnos"
    )
    
