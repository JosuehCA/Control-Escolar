from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from sistema.models.forms_mensajeria import MensajePrivadoForm, MensajeGeneralForm, MensajeGrupalForm
from sistema.models.models_mensajeria import MensajePrivado, MensajeGeneral, MensajeGrupal
from sistema.models.models import Grupo, UsuarioEscolar

def mostrarVistaConversacionPrivada(request: HttpRequest, nombreDeUsuarioReceptor: str) -> HttpResponse:
    """Vista dinamica para conversaciones individuales, grupales o generales."""
    usuarioReceptor:UsuarioEscolar = UsuarioEscolar.obtenerUsuarioSegunNombreDeUsuario(nombreDeUsuarioReceptor)
    mensajesPrivados:MensajePrivado = MensajePrivado.obtenerMensajesEntreUsuarios(request.user, usuarioReceptor)
    return render(request, "sistema/Vista_MensajeriaPrivada.html", {
        "form": MensajePrivadoForm(),
        "mensajes": mensajesPrivados,
        "nombreDeUsuarioReceptor": nombreDeUsuarioReceptor})
    
        
def mostrarVistaConversacionGrupal(request: HttpRequest, grupoReceptor: str) -> HttpResponse:
    """Vista para conversaciones individuales."""
    grupoReceptorInstancia:Grupo = Grupo.obtenerGrupoSegunNombre(grupoReceptor)
    mensajesGrupales:MensajeGrupal = MensajeGrupal.obtenerMensajesDeGrupo(grupoReceptorInstancia)
    return render(request, "sistema/Vista_MensajeriaGrupal.html", {
        "form": MensajeGrupalForm(),
        "mensajes": mensajesGrupales,
        "grupoReceptor": grupoReceptor})

def mostrarVistaConversacionGeneral(request: HttpRequest) -> HttpResponse:
    """Vista para conversaciones generales."""
    mensajesGenerales = MensajeGeneral.obtenerMensajesGenerales()
    return render(request, "sistema/Vista_MensajeriaGeneral.html", {
        "form": MensajeGeneralForm(),
        "mensajes": mensajesGenerales})
