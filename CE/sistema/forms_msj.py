from django import forms
from .mensaje import MensajeDirecto, MensajeGrupo

# Formulario para enviar un mensaje directo
class MensajeDirectoForm(forms.ModelForm):
    class Meta:
        model = MensajeDirecto
        fields = ['receptor', 'contenido']

# Formulario para enviar un mensaje a un grupo
class MensajeGrupoForm(forms.ModelForm):
    class Meta:
        model = MensajeGrupo
        fields = ['grupos', 'contenido']