from django import forms

from sistema.models.models import Alumno, Grupo
from .models import *
from django.core.exceptions import ValidationError 
from sistema.models.models import *


        
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
    

class PaseDeListaForm(forms.Form):
    def __init__(self, grupo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for alumno in grupo.alumnos.all():
            self.fields[f'asistencias_{alumno.id}'] = forms.BooleanField(
                label=f"{alumno.getNombre()}",
                required=False
            )

class AsignarCalificacionForm(forms.ModelForm):
    class Meta:
        model = RegistroCalificaciones
        fields = ['alumno', 'calificacion', 'comentario']

    calificacion = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 6)], label="Calificación")
    comentario = forms.CharField(required=False, widget=forms.Textarea, label="Comentario")
