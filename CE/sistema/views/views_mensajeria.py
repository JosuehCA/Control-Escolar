from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from sistema.models.forms_mensajeria import MensajeDirectoForm, MensajeGeneralForm, MensajeGrupalForm
from sistema.models.models_mensajeria import MensajeDirecto, ManejadorVistaMensajeria, MensajeGeneral, MensajeGrupal
from sistema.models.models import Grupo

def mostrarVistaConversacionPrivada(request: HttpRequest, nombreDeUsuarioReceptor: str) -> HttpResponse:
    """Vista dinamica para conversaciones individuales, grupales o generales."""
    manejador = ManejadorVistaMensajeria()
    tipoDeConversacion = manejador.obtenerTipoDeConversacion(nombreDeUsuarioReceptor)
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
                "form": mensajeDirectoForm,
                "servicioDeMensajeriaURL": nombreDeUsuarioReceptor,})
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
                "servicioDeMensajeriaURL": nombreDeUsuarioReceptor,})
        
        elif(tipoDeConversacion == "grupo"):
            mensajesUsuario = MensajeDirecto.obtenerMensajesFiltrados(request.user)

            return render(request, "sistema/Vista_Conversacion.html", {
                "titulo": "Conversación Grupal",
                "mensajes": mensajesUsuario,})
        
        else:
            return render(request, "sistema/Vista_Conversacion.html", {
                "titulo": "Conversación General",
                "mensajes": MensajeDirecto.obtenerMensajesFiltrados(request.user),})
        
def mostrarVistaConversacionGrupal(request: HttpRequest, grupoReceptor: str) -> HttpResponse:
    """Vista para conversaciones individuales."""
    mensajeGrupalForm = MensajeGrupalForm()
    grupoReceptorInstancia = Grupo.objects.get(nombre=grupoReceptor)
    mensajesGrupales = MensajeGrupal.obtenerMensajesFiltrados(grupoReceptorInstancia)
    print(mensajesGrupales)
    return render(request, "sistema/Vista_MensajeriaGrupal.html", {
        "titulo": "Conversación Grupal",
        "form": mensajeGrupalForm,
        "mensajes": mensajesGrupales,
        "grupoReceptor": grupoReceptor,})

def mostrarVistaConversacionGeneral(request: HttpRequest) -> HttpResponse:
    """Vista para conversaciones generales."""

    mensajeGeneralForm = MensajeGeneralForm()
    mensajesGenerales = MensajeGeneral.obtenerMensajesFiltrados()

    return render(request, "sistema/Vista_MensajeriaGeneral.html", {
        "titulo": "Conversación General",
        "form": mensajeGeneralForm,
        "mensajes": mensajesGenerales,})
