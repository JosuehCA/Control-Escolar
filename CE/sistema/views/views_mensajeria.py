from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from sistema.forms_msj import MensajeDirectoForm
from sistema.models.models_msj import MensajeDirecto

@login_required
def enviarMensajeDirecto(request: HttpRequest) -> HttpResponse:
    """Vista para enviar un mensaje directo."""

    if request.method == 'POST':
        mensajeDirectoForm = MensajeDirectoForm(request.POST)
        
        if mensajeDirectoForm.is_valid():
            mensajeDirectoInstancia = mensajeDirectoForm.save(commit=False)
            receptorUsuario = mensajeDirectoForm.cleaned_data.get('receptorUsuario')
            
            if mensajeDirectoInstancia.enviar(request.user, receptorUsuario):
                return redirect('mensaje_directo')
            else:
                mensajeDirectoForm.add_error(None, "No puedes enviarte mensajes a ti mismo.")
    
    else:
        mensajeDirectoForm = MensajeDirectoForm()

    mensajesUsuario = MensajeDirecto.obtenerMensajesFiltrados(request.user)

    return render(request, 'sistema/testMensajeria.html', {
        'form': mensajeDirectoForm,
        'mensajes': mensajesUsuario,
    })