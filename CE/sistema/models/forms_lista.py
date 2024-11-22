from django import forms
from sistema.models.models import Alumno

class AsistenciaForm(forms.Form):
    alumno = forms.ModelChoiceField(queryset=Alumno.objects.all(), label="Alumno")
    asistencias = forms.IntegerField(min_value=0, label="Asistencias")
    faltas = forms.IntegerField(min_value=0, label="Faltas")