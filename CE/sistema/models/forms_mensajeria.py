from django import forms
from .models_mensajeria import MensajePrivado, MensajeGrupal, MensajeGeneral

# Formulario para enviar un mensaje directo
class MensajePrivadoForm(forms.ModelForm):
    class Meta:
        model = MensajePrivado
        fields = ['receptorUsuario', 'contenidoMensaje']

# Formulario para enviar un mensaje a un grupo
class MensajeGrupalForm(forms.ModelForm):
    class Meta:
        model = MensajeGrupal
        fields = ['grupoRelacionado', 'contenidoMensaje']

# Formulario para enviar un mensaje general
class MensajeGeneralForm(forms.ModelForm):
    class Meta:
        model = MensajeGeneral
        fields = ['contenidoMensaje']