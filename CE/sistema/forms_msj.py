from django import forms
from .models.models_msj import MensajeDirecto, MensajeGrupo

# Formulario para enviar un mensaje directo
class MensajeDirectoForm(forms.ModelForm):
    class Meta:
        model = MensajeDirecto
        fields = ['receptorUsuario', 'contenidoMensaje']

# Formulario para enviar un mensaje a un grupo
class MensajeGrupoForm(forms.ModelForm):
    class Meta:
        model = MensajeGrupo
        fields = ['gruposRelacionados', 'contenidoMensaje']
