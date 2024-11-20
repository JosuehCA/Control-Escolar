from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from CE.sistema.forms_mensajeria import MensajeDirectoForm
from CE.sistema.models.models_mensajeria import MensajeDirecto
from CE.sistema.views.views_mensajeria import ManejadorVistaMensajeria

def mostrarVistaConversacion(request: HttpRequest, servicioDeMensajeriaURL: str) -> HttpResponse:
    """Vista dinamica para conversaciones individuales, grupales o generales."""
    manejador = ManejadorVistaMensajeria()
    tipoDeConversacion = manejador.obtenerTipoDeConversacion(servicioDeMensajeriaURL)
    if request.method == 'POST':
        mensajeDirectoForm = MensajeDirectoForm(request.POST)
        mensajesUsuario = MensajeDirecto.obtenerMensajesFiltrados(request.user)
        
        if mensajeDirectoForm.is_valid():
            mensajeDirectoInstancia = mensajeDirectoForm.save(commit=False)
            receptorUsuario = mensajeDirectoForm.cleaned_data.get('receptorUsuario')
            
            if mensajeDirectoInstancia.enviar(request.user, receptorUsuario):
                return render(request, "sistema/Vista_Conversacion.html", {
                "titulo": "Conversación Privada",
                "mensajes": mensajesUsuario,
                "form": mensajeDirectoForm,})
            else:
                mensajeDirectoForm.add_error(None, "No puedes enviarte mensajes a ti mismo.")
    else:
        if(tipoDeConversacion == "privado"):
            mensajeDirectoForm = MensajeDirectoForm()
            mensajesUsuario = MensajeDirecto.obtenerMensajesFiltrados(request.user)

            return render(request, "sistema/Vista_Conversacion.html", {
                "titulo": "Conversación Privada",
                "mensajes": mensajesUsuario,
                "form": mensajeDirectoForm,
                "servicioDeMensajeriaURL": servicioDeMensajeriaURL,})
        
        elif(tipoDeConversacion == "grupo"):
            mensajesUsuario = MensajeDirecto.obtenerMensajesFiltrados(request.user)

            return render(request, "sistema/Vista_Conversacion.html", {
                "titulo": "Conversación Grupal",
                "mensajes": mensajesUsuario,})
        
        else:
            return render(request, "sistema/Vista_Conversacion.html", {
                "titulo": "Conversación General",
                "mensajes": MensajeDirecto.obtenerMensajesFiltrados(request.user),})
