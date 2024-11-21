from django import forms
from .models_mensajeria import MensajeDirecto, MensajeGrupo, MensajeGeneral

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

# Formulario para enviar un mensaje general
class MensajeGeneralForm(forms.ModelForm):
    class Meta:
        model = MensajeGeneral
        fields = ['contenidoMensaje']
