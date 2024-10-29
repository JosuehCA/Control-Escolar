from django.db import models as m
from django.conf import settings
from sistema.models import UsuarioEscolar, Grupo

class Mensaje(m.Model):
    """TDA Mensaje. Define la estructura de un mensaje dentro del mensajero virtual."""

    emisorUsuario = m.ForeignKey(UsuarioEscolar, on_delete=m.CASCADE)
    contenidoMensaje = m.CharField(max_length=2000)
    fechaEnviado = m.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Representación en cadena de un mensaje."""
        return f"Mensaje de {self.emisorUsuario} enviado en {self.fechaEnviado}"

    class Meta:
        abstract = True



class MensajeDirecto(Mensaje):
    """TDA Mensaje Directo. Particulariza un mensaje de manera individual."""
    receptorUsuario = m.ForeignKey(UsuarioEscolar, on_delete=m.DO_NOTHING, related_name="receptor")

    def enviar(self, emisor: UsuarioEscolar, receptor: UsuarioEscolar) -> bool:
        """Envía un mensaje directo si el emisor y el receptor no son el mismo usuario."""
        if not self.es_valido_para_envio(emisor, receptor):
            return False
        self.emisorUsuario = emisor
        self.receptorUsuario = receptor
        self.save()
        return True
    
    def es_valido_para_envio(self, emisor: UsuarioEscolar, receptor: UsuarioEscolar) -> bool:
        """
        Verifica si el mensaje es válido para ser enviado, asegurando que el emisor y receptor sean distintos.
        """
        return emisor != receptor
    
    @staticmethod
    def obtenerMensajesFiltrados(usuario: UsuarioEscolar) -> m.QuerySet:
        """Obtiene los mensajes filtrados que fueron enviados a un usuario específico."""
        return MensajeDirecto.objects.filter(receptorUsuario=usuario).order_by('-fechaEnviado')
    
    def __str__(self) -> str:
        """Representación en cadena de un mensaje directo."""
        return f"Mensaje directo de {self.emisorUsuario} a {self.receptorUsuario}"
    
    class Meta:
        verbose_name = "Mensaje Directo"
        verbose_name_plural = "Mensajes: Directos"



class MensajeGrupo(Mensaje):
    """TDA Mensaje de Grupo. Particulariza un mensaje de manera grupal."""

    gruposRelacionados = m.ManyToManyField(Grupo, related_name="mensajes")


    class Meta:
        verbose_name = "Mensaje Grupo"
        verbose_name_plural = "Mensajes: Grupos"



class MensajePlantel(Mensaje):
    """TDA Mensaje Plantel. Establece un mensaje compartido de manera global a todo el plantel."""

    pass


    class Meta:
        verbose_name = "Mensaje Plantel"
        verbose_name_plural = "Mensajes: Plantel"



class Mensajero(m.Model):
    """TDA Mensajero. Modela el mensajero virtual presente en el sistema y propio de cada usuario 
    registrado."""

    pass



class Conversacion(m.Model):
    """TDA Conversacion. Representa una conversacion individual entre dos partes registradas en el sistema."""

    usuarioPrimario = m.ForeignKey(UsuarioEscolar, on_delete=m.DO_NOTHING, related_name="usuarioPrimario_convo")
    usuarioSecundario= m.ForeignKey(UsuarioEscolar, on_delete=m.DO_NOTHING, related_name="usuarioSecundario_convo")


    class Meta:
        verbose_name = "Conversacion"
        verbose_name_plural = "Conversaciones"



class Notificacion(m.Model):
    """TDA Notificacion. Representa una notificación en particular."""

    def notificar_usuario():
        """Notifica a un usuario en particular."""
        pass


    class Meta:
        verbose_name = "Notificacion"
        verbose_name_plural = "Notificaciones"