from django.db import models as m
from django.conf import settings
from sistema.models.models import UsuarioEscolar, Grupo
from django.http import HttpRequest

class ManejadorVistaMensajeria:
    """TDA Manejador de Vista de Mensajería. Controla la vista de mensajería del sistema."""

    def __init__(self) -> None:
        """Inicializa un manejador de vista de mensajería."""
        
    def obtenerTipoDeConversacion(self, servicioDeMensajeria: str) -> str:
        """Devuelve el tipo de conversación a mostrar."""
        return self.__separarTipoDeUrl(servicioDeMensajeria)[0]
    
    def __separarTipoDeUrl(self, cadenaUrl: str) -> tuple:
        """Separa la variable de la URL por "_" ."""
        return cadenaUrl.split("_")

class Mensaje(m.Model):
    """TDA Mensaje. Define la estructura de un mensaje dentro del mensajero virtual."""

    emisorUsuario = m.ForeignKey(UsuarioEscolar, on_delete=m.CASCADE)
    contenidoMensaje = m.CharField(max_length=2000)
    fechaEnviado = m.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Representación en cadena de un mensaje."""
        return f"Mensaje de {self.emisorUsuario} enviado en {self.fechaEnviado}"
    
    def establecer_contenido(self, contenido: str) -> None:
        """Establece el contenido de un mensaje."""
        self.contenidoMensaje = contenido

    def almacenarEnBaseDeDatos(self) -> None:
        """Almacena el mensaje en la base de datos."""
        self.save()

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
        self.almacenarEnBaseDeDatos()
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

    gruposRelacionados = m.ForeignKey(Grupo, on_delete=m.DO_NOTHING, related_name="mensajes")

    @staticmethod
    def obtenerMensajesFiltrados(grupo: Grupo) -> m.QuerySet:
        """Obtiene los mensajes filtrados que fueron enviados a un grupo específico."""
        return MensajeGrupo.objects.filter(grupoRelacionado=grupo).order_by('-fechaEnviado')

    class Meta:
        verbose_name = "Mensaje Grupo"
        verbose_name_plural = "Mensajes: Grupos"



class MensajeGeneral(Mensaje):
    """TDA Mensaje Plantel. Establece un mensaje compartido de manera global a todo el plantel."""

    @staticmethod
    def obtenerMensajesFiltrados() -> m.QuerySet:
        """Obtiene los mensajes filtrados que fueron enviados a todo el plantel."""
        return MensajeGeneral.objects.all().order_by('-fechaEnviado')
    
    def diccionarioAMensaje(self, datos: dict) -> None:
        """Convierte un diccionario a un mensaje."""
        self.emisorUsuario = datos['emisorusuario']
        self.contenidoMensaje = datos['contenidoMensaje']
        self.fechaEnviado = datos['fechaEnviado']


    class Meta:
        verbose_name = "Mensaje General"
        verbose_name_plural = "Mensajes: Generales"

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