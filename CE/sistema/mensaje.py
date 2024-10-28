from django.db import models as m
from django.conf import settings
from sistema.models import UsuarioEscolar, Grupo

class Mensaje(m.Model):
    """TDA Mensaje. Define la estructura de un mensaje dentro del mensajero virtual."""

    emisor = m.ForeignKey(UsuarioEscolar, on_delete=m.CASCADE)
    contenido = m.CharField(max_length=2000)
    fechaEnviado = m.DateTimeField(auto_now_add=True)


    class Meta:
        abstract = True



class MensajeDirecto(Mensaje):
    """TDA Mensaje Directo. Particulariza un mensaje de manera individual."""# Maybe añadir vistos?
    receptor = m.ForeignKey(UsuarioEscolar, on_delete=m.DO_NOTHING, related_name="receptor")
    

    class Meta:
        verbose_name = "Mensaje Directo"
        verbose_name_plural = "Mensajes: Directos"



class MensajeGrupo(Mensaje):
    """TDA Mensaje de Grupo. Particulariza un mensaje de manera grupal."""

    grupos = m.ManyToManyField(Grupo, related_name="mensajes")


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

    usuario1 = m.ForeignKey(UsuarioEscolar, on_delete=m.DO_NOTHING, related_name="usuario1_convo")
    usuario2 = m.ForeignKey(UsuarioEscolar, on_delete=m.DO_NOTHING, related_name="usuario2_convo")


    class Meta:
        verbose_name = "Conversacion"
        verbose_name_plural = "Conversaciones"



class Notificacion(m.Model):
    """TDA Notificacion. Representa una notificación en particular."""

    def notificar_usuario(sender, instance, **kwargs):
        """Notifica a un usuario en particular."""
        pass


    class Meta:
        verbose_name = "Notificacion"
        verbose_name_plural = "Notificaciones"