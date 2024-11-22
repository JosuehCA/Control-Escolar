from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from sistema.models.forms_mensajeria import MensajePrivadoForm, MensajeGeneralForm, MensajeGrupalForm
from sistema.models.models_mensajeria import MensajePrivado, MensajeGeneral, MensajeGrupal
from sistema.models.models import Grupo, UsuarioEscolar

def mostrarVistaConversacionPrivada(request: HttpRequest, nombreDeUsuarioReceptor: str) -> HttpResponse:
    """Vista dinamica para conversaciones individuales, grupales o generales."""
    mensajePrivadoForm = MensajePrivadoForm()
    usuarioReceptor = UsuarioEscolar.objects.get(username=nombreDeUsuarioReceptor)
    mensajesPrivados = MensajePrivado.obtenerMensajesEntreUsuarios(request.user, usuarioReceptor)
    return render(request, "sistema/Vista_MensajeriaPrivada.html", {
        "form": mensajePrivadoForm,
        "mensajes": mensajesPrivados,
        "nombreDeUsuarioReceptor": nombreDeUsuarioReceptor,})
    
        
def mostrarVistaConversacionGrupal(request: HttpRequest, grupoReceptor: str) -> HttpResponse:
    """Vista para conversaciones individuales."""
    mensajeGrupalForm = MensajeGrupalForm()
    grupoReceptorInstancia = Grupo.objects.get(nombre=grupoReceptor)
    mensajesGrupales = MensajeGrupal.obtenerMensajesDeGrupo(grupoReceptorInstancia)
    print(mensajesGrupales)
    return render(request, "sistema/Vista_MensajeriaGrupal.html", {
        "form": mensajeGrupalForm,
        "mensajes": mensajesGrupales,
        "grupoReceptor": grupoReceptor,})

def mostrarVistaConversacionGeneral(request: HttpRequest) -> HttpResponse:
    """Vista para conversaciones generales."""

    mensajeGeneralForm = MensajeGeneralForm()
    mensajesGenerales = MensajeGeneral.obtenerMensajesGenerales()

    return render(request, "sistema/Vista_MensajeriaGeneral.html", {
        "form": mensajeGeneralForm,
        "mensajes": mensajesGenerales,})
